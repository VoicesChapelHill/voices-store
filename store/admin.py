from django.contrib import admin
from store.models import Product, Price, OrderLine, Sale

admin.site.register(Product)
admin.site.register(Price)
admin.site.register(OrderLine)
admin.site.register(Sale)
