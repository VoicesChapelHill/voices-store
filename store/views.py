from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
# from django.utils.timezone import now

# import stripe

# from store.email import send_sale_email
#from store.forms import BuySomethingForm, DonationForm, MemberLoginForm
from django.utils.timezone import now
from django.views.decorators.http import require_GET, require_POST
import stripe
from store.email import send_sale_email
from store.forms import MemberLoginForm, ContactForm, OrderLineForm
from store.models import Product, OrderLine, Sale
from store.utils import log_member_in, get_sale
from users.views import please_login


def member_login(request, next):
    if not request.user.is_authenticated():
        return please_login(request)
    if request.user.is_member:
        messages.info(request, "You are a Voices member")
        return redirect(next or reverse('store'))
    form = MemberLoginForm(
        data=request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST' and form.is_valid():
        log_member_in(request)
        return redirect(next or reverse('store'))
    return render(request, 'store/member_login.html', {'form': form})


@require_GET
def store_view(request):
    user = request.user
    TIME = now()
    query = ((Q(sell_stop__gte=TIME) | Q(sell_stop=None))
             & (Q(sell_start__lte=TIME) | Q(sell_start=None)))
    if user.is_authenticated() and user.voices_staff:
        query |= Q(draft=True)
    products = Product.objects.filter(query)

    if user.is_authenticated() and user.is_member:
        title = 'Member Store'
    else:
        title = 'Voices Store'
        products = products.exclude(member_only=True)

    if not user.is_authenticated() or not user.is_staff:
        products = products.exclude(draft=True)

    context = {
        'products': products,
        'title': title,
    }
    return render(request, 'store/store.html', context)


@require_POST
def remove_view(request, item_pk):
    order_line = get_object_or_404(OrderLine, pk=item_pk)
    order_line.delete()
    return redirect(reverse('review'))


@login_required
def review_view(request):
    """
    GET: review what user is about to buy
    POST: buy it
    """
    sale = get_sale(request)
    if not sale or sale.is_empty():
        messages.info(request, "Cart is empty")
        return redirect(reverse('store'))
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
        'lines': sale.orderline_set.order_by('product'),
        'amount_in_cents': amount_in_cents,
        'stripe_key': settings.STRIPE_PUBLISHABLE_KEY,
        'cart': sale,
        'PRICE_ONE': Product.PRICE_ONE,
        'PRICE_MULTIPLE': Product.PRICE_MULTIPLE,
        'PRICE_USER': Product.PRICE_USER,
    }
    return render(request, 'store/review.html', context)
#
#
# def complete_view(request, key):
#     """
#     Show a completed sale
#     """
#
#     # 'key' is the charge_id
#     sale = get_object_or_404(Sale, charge_id=key)
#
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     charge = stripe.Charge.retrieve(key, expand=['card'])
#
#     context = {
#         'sale': sale,
#         'charge': charge,
#     }
#     return render(request, 'store/complete.html', context)


def empty_view(request):
    raise NotImplementedError  # FIXME


@require_GET
def help_view(request):
    return render(request, 'help.html')


def contact_view(request):
    if request.user.is_authenticated():
        email = request.user.email
    else:
        email = None
    if request.method == 'POST':
        form = ContactForm(email=email, data=request.POST)
        if form.is_valid():
            subject = "Contact form: %s" % form.cleaned_data['subject']
            email = form.cleaned_data['email_address']
            body = render_to_string('emails/contact_form.txt',
                                    {'body': form.cleaned_data['body'],
                                     'email': email,
                                     'user': request.user})
            send_mail(
                subject=subject,
                message=body,
                from_email=email,
                recipient_list=settings.CONTACT_EMAILS,
            )
            messages.info(
                request,
                "Thank you!  Your message has been sent to the site administrators. "
                "If you have a question or problem, someone will contact you.")
            return redirect(request.path)
    else:
        form = ContactForm(email=email)
    return render(request, 'contact.html', {'form': form})


def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.draft and (not request.user.is_authenticated() or not request.user.is_staff):
        raise Http404
    if product.member_only and (not request.user.is_authenticated() or not request.user.is_member):
        raise Http404

    sale = get_sale(request) or Sale()

    if sale.pk and product.quantifiable:
        # See if we have any order lines already saved for this product
        # if it's quantifiable. Otherwise, we don't let them edit it except
        # by going to the cart and deleting it; instead, they can add a new
        # one.
        order_lines = []
        for price in product.prices.all():
            try:
                order_lines.append(OrderLine.objects.get(sale=sale, product=product, price=price))
            except OrderLine.DoesNotExist:
                order_lines.append(OrderLine(product=product, price=price))
        if not order_lines:
            try:
                order_lines.append(OrderLine.objects.get(sale=sale, product=product, price=None))
            except OrderLine.DoesNotExist:
                order_lines.append(OrderLine(product=product, price=None))
    else:
        order_lines = [OrderLine(product=product, price=price) for price in product.prices.all()]
        if not order_lines:
            order_lines.append(OrderLine(product=product))

    if request.method == 'POST':
        forms = [OrderLineForm(instance=x, data=request.POST) for x in order_lines]
        if all(form.is_valid() for form in forms):
            print("VALID!")  # FIXME
            # Did they actually order anything?
            if any(form.has_any() for form in forms):
                # YES!
                # We want a sale!
                if not sale.pk:
                    sale = Sale.objects.create()
                for form in forms:
                    if form.has_any():
                        form.instance.sale = sale
                        form.save()
            # Did they change any existing items to zero?
            for form in forms:
                if not form.has_any():
                    if form.instance.pk:
                        form.instance.delete()
            if sale.pk:
                response = HttpResponseRedirect(reverse('store'))
                response.set_signed_cookie('sale', sale.pk, salt=settings.SECRET_KEY)
                return response
            return redirect(reverse('store'))
        else:
            print("SOME FORM IS NOT VALID")  # FIXME
            for form in forms:
                print(form.errors)
    else:
        forms = [OrderLineForm(instance=x) for x in order_lines]

    context = {
        'product': product,
        'forms': forms,
        'sale': sale,
        'PRICE_ONE': Product.PRICE_ONE,
        'PRICE_MULTIPLE': Product.PRICE_MULTIPLE,
        'PRICE_USER': Product.PRICE_USER,
    }
    response = render(request, 'store/product.html', context)
    if sale.pk:
        response.set_signed_cookie('sale', sale.pk, salt=settings.SECRET_KEY)
    return response
