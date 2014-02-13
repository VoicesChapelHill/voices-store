from django.contrib import admin
from django.utils.translation import ugettext as _

from users.models import VoicesUser


admin.site.register(
    VoicesUser,
    filter_horizontal=('groups', 'user_permissions',),
    list_display=['email', 'last_name', 'first_name', 'is_member', 'voices_staff', 'is_staff'],
    list_filter=('is_member', 'is_staff', 'is_superuser', 'voices_staff'),
    search_fields=('first_name', 'last_name', 'email'),
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_member', 'is_active', 'voices_staff',
                                       'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
)
