from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from users.views import ProfileView, logged_in_view, delete_account_view


urlpatterns = patterns(
    '',
    url(r'^profile/(?P<pk>\d+)$',
        login_required(ProfileView.as_view()),
        name='profile'),
    url(r'^logged_in/$', logged_in_view, name='logged_in'),
    url(r'^delete/$', delete_account_view, name='delete_account'),
)
