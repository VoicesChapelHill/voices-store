
from django.contrib.auth.decorators import login_required


# FIXME: require voices staff
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView


@login_required
def home(request):
    context = {
    }
    return render(request, 'staff/home.html', context)
