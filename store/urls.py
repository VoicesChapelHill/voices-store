from django.conf.urls import patterns, url

from store.views import empty_view, review_view, remove_view, store_view, member_login, help_view, contact_view, product_view

urlpatterns = patterns(
    '',
    url(r'^$', store_view, name='store'),
    url(r'^product/(?P<slug>.*)/$', product_view, name='product'),
    url(r'^member_login/(?P<next>.*)/$', member_login, name='member_login'),
    url(r'^review/$', review_view, name='review'),
    url(r'^remove/(?P<item_pk>.*)/$', remove_view, name='remove'),
    url(r'^empty/$', empty_view, name='empty'),
    # url(r'^complete/(?P<key>.*)/$', complete_view, name='complete'),

    url(r'^staff/$', store_view, name='staff_home'),  # FIXME
    url(r'^help/$', help_view, name='help'),
    url(r'^contact/$', contact_view, name='contact'),
)
