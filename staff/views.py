
from django.contrib.auth.decorators import login_required


# FIXME: require voices staff
from django.shortcuts import render, get_object_or_404
from store.models import ProductGroup


@login_required
def home(request):
    context = {
        'product_groups': ProductGroup.objects.all(),
    }
    return render(request, 'staff/home.html', context)


def group_report(request, group_pk):
    group = get_object_or_404(ProductGroup, pk=group_pk)
    context = {
        'group': group,
    }
    return render(request, 'staff/group.html', context)
