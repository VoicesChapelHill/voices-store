from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
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


@login_required
def logged_in_view(request):
    """User has just logged in"""
    user = request.user
    if user.is_complete():
        return redirect(reverse('store'))
    messages.info(request, "Please tell us a little more about yourself")
    return redirect(reverse('profile', args=[user.pk]))
