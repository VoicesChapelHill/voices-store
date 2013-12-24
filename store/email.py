from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
import stripe


def send_sale_email(sale):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge = stripe.Charge.retrieve(sale.charge_id, expand=['card'])

    context = {
        'sale': sale,
        'charge': charge,
    }

    body = render_to_string('store/complete.txt', context)
    recipients = sale.emails_to_notify()

    send_mail('Voices purchase', body, 'from@example.com',
              list(recipients), fail_silently=False)
