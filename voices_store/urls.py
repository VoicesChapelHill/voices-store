from warnings import warn
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^staff/', include('staff.urls', app_name='staff')),
     (r'', include('django_browserid.urls')),
    url(r'^', include('store.urls')),
)


# make sure required settings are set
required = ['STRIPE_SECRET_KEY', 'STRIPE_PUBLISHABLE_KEY', 'MEMBER_PASSWORD',
            'CONTACT_EMAILS']
for name in required:
    if not hasattr(settings, name):
        warn("Required setting '%s' is missing. Required settings are %r" % (name, required))
