# TBD
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from users.views import please_login


def home(request):
    if not request.user.is_authenticated():
        return please_login(request)
    if not request.user.voices_staff:
        messages.error(request, "Sorry, you're not authorized for that page")
        return redirect(reverse('store'))
    context = {
    }
    return render(request, 'staff/home.html', context)
