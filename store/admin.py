from django.contrib import admin
from store.models import Product, Price, OrderLine, Sale

admin.site.register(
    Product,
    list_display=['name', 'member_only', 'sell_start', 'sell_stop', 'draft', 'pricing'],
    prepopulated_fields={"slug": ("name",)},
)
admin.site.register(Price)
admin.site.register(OrderLine)
admin.site.register(Sale)
