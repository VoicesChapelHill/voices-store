from decimal import Decimal
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from store.models import ItemSale


class ItemSaleForm(forms.ModelForm):
    class Meta:
        model = ItemSale
        fields = ['quantity']


class BuySomethingForm(forms.Form):
    quantity = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={'size': '4',
                   'min': '0',
                   'max': '100',
                   }
        )
    )


class DonationForm(forms.Form):
    amount = forms.DecimalField(
        required=False,
        decimal_places=2,
        min_value=Decimal('0.00'),
        widget=forms.TextInput(
            attrs={'size': '6'}
        )
    )


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
