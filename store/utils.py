from django.conf import settings
from store.models import Sale


def log_member_in(request):
    if not request.user.is_member:
        request.user.is_member = True
        request.user.save()


def get_sale(request):
    sale = None

    sale_pk = request.get_signed_cookie('sale', salt=settings.SECRET_KEY, default=None,
                                        max_age=3600)
    if sale_pk:
        try:
            sale = Sale.objects.get(pk=sale_pk, status=Sale.SALE_PENDING)
        except Sale.DoesNotExist:
            pass
    return sale


def cart_template_context(request):
    return {'sale': get_sale(request)}
