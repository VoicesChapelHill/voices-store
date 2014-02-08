from decimal import Decimal
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
#from store.models import ItemSale

#
# class ItemSaleForm(forms.ModelForm):
#     class Meta:
#         model = ItemSale
#         fields = ['quantity']
#
#
# class BuySomethingForm(forms.Form):
#     quantity = forms.IntegerField(
#         required=False,
#         widget=forms.NumberInput(
#             attrs={'size': '4',
#                    'min': '0',
#                    'max': '100',
#                    }
#         )
#     )
#
#     def __init__(self, product, *args, **kwargs):
#         self.product = product
#         super().__init__(*args, **kwargs)
#
#     def add_to_sale(self, sale):
#         if not self.is_valid():
#             return
#         quantity = self.cleaned_data['quantity'] or 0
#         if quantity > 0:
#             if not sale.pk:
#                 sale.save()
#             product = self.product
#             if sale.items.filter(product=product).exists():
#                 item_sale = sale.items.get(product=product)
#                 item_sale.quantity = quantity
#                 item_sale.per_item_price = product.price
#                 item_sale.save()
#             else:
#                 ItemSale.objects.create(
#                     product=product,
#                     sale=sale,
#                     quantity=quantity,
#                     per_item_price=product.price,
#                 )
#
#
# class DonationForm(forms.Form):
#     amount = forms.DecimalField(
#         required=False,
#         decimal_places=2,
#         min_value=Decimal('0.00'),
#         widget=forms.TextInput(
#             attrs={'size': '6'}
#         )
#     )
#
#     def __init__(self, product, *args, **kwargs):
#         self.product = product
#         super().__init__(*args, **kwargs)
#
#     def add_to_sale(self, sale):
#         if not self.is_valid():
#             return
#         amount = self.cleaned_data['amount'] or Decimal('0.00')
#         quantity = 100 * amount
#         if quantity > 0:
#             product = self.product
#             if not sale.pk:
#                 sale.save()
#             if sale.items.filter(product=product).exists():
#                 item_sale = sale.items.get(product=product)
#                 item_sale.quantity = quantity
#                 item_sale.per_item_price = product.price
#                 item_sale.save()
#             else:
#                 ItemSale.objects.create(
#                     product=product,
#                     sale=sale,
#                     quantity=quantity,
#                     per_item_price=product.price,
#                 )
#


class MemberLoginForm(forms.Form):
    password = forms.CharField(
        max_length=20,
        widget=PasswordInput
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if password != settings.MEMBER_PASSWORD:
            raise ValidationError("Member password is not correct")
        return password
