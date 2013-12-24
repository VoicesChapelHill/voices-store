from django.conf.urls import patterns, url

from store.views import review_view, store_view, complete_view, member_login

urlpatterns = patterns(
    '',
    url(r'^$', store_view, name='store', kwargs={'pagename': 'public'}),
    url(r'^members/$', store_view, name='member_view', kwargs={'pagename': 'member'}),
    url(r'^member_login/(?P<next>.*)/$', member_login, name='member_login'),
    url(r'^review/$', review_view, name='review'),
    url(r'^complete/(?P<key>.*)/$', complete_view, name='complete'),
)
