from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.views.generic import UpdateView
from users.models import VoicesUser


class ProfileView(UpdateView):
    model = VoicesUser
    fields = [
        'first_name',
        'last_name',
    ]

    def get_success_url(self):
        messages.info(self.request, 'Your information has been updated, thank you')
        return reverse('store')


def please_login(request):
    context = {
        'next': request.path,
    }
    return render(request, "please_login.html", context)


def logged_in_view(request):
    """User has just logged in"""
    user = request.user
    if user.is_complete():
        return redirect(reverse('store'))
    messages.info(request, "Please tell us a little more about yourself")
    return redirect(reverse('profile', args=[user.pk]))


def delete_account_view(request):
    if not request.user.is_authenticated():
        return please_login(request)
    messages.info(request, "To delete your account, please use the contact form "
                           "and ask us to delete your account.")
    return redirect(reverse('contact'))
