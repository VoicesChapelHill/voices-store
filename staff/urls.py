from django.conf.urls import patterns, url

urlpatterns = patterns(
    'staff.views',
    url(r'^$', 'home', name='staff_home'),
    url(r'^group/(?P<group_pk>.*)/$', 'group_report', name='group_report'),
)
