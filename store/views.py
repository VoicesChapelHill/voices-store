from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

import stripe

from store.email import send_sale_email
from store.forms import BuySomethingForm, DonationForm, MemberLoginForm
from store.models import Product, Sale, ItemSale
from store.utils import log_member_in, member_is_logged_in


def member_login(request, next):
    form = MemberLoginForm(
        data=request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST' and form.is_valid():
        log_member_in(request)
        return redirect(next)
    return render(request, 'store/member_login.html', {'form': form})


def store_view(request, pagename):
    if pagename == 'member' and not member_is_logged_in(request):
        return redirect('member_login', next=request.path)

    products = Product.objects.all()

    TIME = now()
    products = products.filter(group__display_start__lte=TIME,
                               group__display_end__gte=TIME)

    if pagename == 'member':
        products = products.filter(group__members=True)
        title = 'Member Store'
    elif pagename == 'public':
        products = products.filter(group__public=True)
        title = 'Voices Store'
    else:
        raise ImproperlyConfigured("Unknown store pagename: %s" % pagename)

    if request.method == 'POST':
        data = request.POST
    else:
        data = None

    forms = []
    for product in products:
        if product.group.donation:
            form = DonationForm(
                prefix=product.pk,
                initial={
                    'amount': Decimal('0.00'),
                },
                data=data
            )
        else:
            form = BuySomethingForm(
                prefix=product.pk,
                initial={
                    'product': product,
                    'quantity': 0,
                },
                data=data
            )
        product.form = form
        forms.append(form)

    if request.method == 'POST':
        if all(form.is_valid() for form in forms):
            sale = Sale()
            for product in products:
                form = product.form
                if product.group.donation:
                    amount = form.cleaned_data['amount'] or Decimal('0.00')
                    quantity = 100 * amount
                else:
                    quantity = form.cleaned_data['quantity'] or 0
                if quantity > 0:
                    if not sale.pk:
                        sale.save()
                    ItemSale.objects.create(
                        product=product,
                        sale=sale,
                        quantity=quantity,
                        per_item_price=product.price,
                    )
            if sale.pk:
                # They're buying something
                # Stick the sale pk in the session
                request.session['sale'] = sale.pk
                return redirect('review')
            messages.info(request, "Didn't order anything")
            return redirect('store')

    context = {
        'products': products,
        'title': title,
    }
    return render(request, 'store/store.html', context)


def review_view(request):
    """
    GET: review what user is about to buy
    POST: buy it
    """
    sale_pk = request.session['sale']
    sale = get_object_or_404(Sale, pk=sale_pk)
    amount_in_cents = int(100 * sale.total())

    if request.method == 'POST':
        # Get the stripe token
        token = request.POST['stripeToken']

        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create the charge on Stripe's servers - this will charge the user's card
        try:
            charge = stripe.Charge.create(
                amount=amount_in_cents,  # amount in cents, again
                currency="usd",
                card=token,
                description="payinguser@example.com",
                metadata={
                    'sale_pk': sale.pk,
                }
            )
        except stripe.error.CardError as e:
            # The card has been declined
            print("DECLINED")
            messages.error(request,
                           "We're sorry, we were not able to charge your card. %s" % e.message)
        else:
            # Remember it
            print("WE SOLD IT!")
            sale.charge_id = charge.id
            if charge.paid:
                sale.complete = True
            sale.save()
            send_sale_email(sale)
            messages.info(request, "Your purchase was successful!  Watch your email for confirmation.")
            del request.session['sale']
            return redirect('store')

    context = {
        'sale': sale,
        'amount_in_cents': amount_in_cents,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'store/review.html', context)


def complete_view(request, key):
    """
    Show a completed sale
    """

    # 'key' is the charge_id
    sale = get_object_or_404(Sale, charge_id=key)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge = stripe.Charge.retrieve(key, expand=['card'])

    context = {
        'sale': sale,
        'charge': charge,
    }
    return render(request, 'store/complete.html', context)
