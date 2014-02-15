# TBD
from django.conf.urls import patterns, url
#from staff.views import SalesListView, SaleDetailView

urlpatterns = patterns(
    'staff.views',
    url(r'$', 'home', name='staff_home'),
    # url(r'^group/(?P<group_pk>.*)/$', 'group_report', name='group_report'),
    #url(r'^sales/$', SalesListView.as_view(template_name='staff/sales.html'), name='sales_report'),
    # url(r'^sale/(?P<pk>.*)/$', SaleDetailView.as_view(template_name='staff/sale_detail.html'), name='sale_detail'),
)
