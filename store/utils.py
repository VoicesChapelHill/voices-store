from store.models import Sale


def log_member_in(request):
    if not request.user.is_member:
        request.user.is_member = True
        request.user.save()


def cart_template_context(request):
    sale = None
    if 'sale_pk' in request.session:
        try:
            sale = Sale.objects.get(pk=request.session['sale_pk'])
        except Sale.DoesNotExist:
            pass
    return {'sale': sale}
