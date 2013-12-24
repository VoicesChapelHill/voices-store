from django.contrib import admin
from store.models import ProductGroup, Product, Sale, Customer, ItemSale


class ItemSaleInline(admin.TabularInline):
    model = ItemSale


class ProductInline(admin.TabularInline):
    model = Product


admin.site.register(Customer)
admin.site.register(ItemSale)
admin.site.register(
    Sale,
    inlines=[ItemSaleInline],
    list_display=['when', 'complete', 'total', 'who'],
    list_filter=['complete']
)
admin.site.register(Product)

admin.site.register(
    ProductGroup,
    filter_horizontal=['to_notify'],
    inlines=[ProductInline]
)
