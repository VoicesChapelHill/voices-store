from decimal import Decimal
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import PasswordInput
from django.utils.translation import ugettext as _
from store.models import OrderLine, Product


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


class SetFieldClassesMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set html class and placeholder
        for field in self.fields.values():
            classes = set(field.widget.attrs.get('class', '').split())
            classes.add('form-control')
            if field.required:
                classes.add('required')
            field.widget.attrs['class'] = ' '.join(list(classes))
            field.widget.attrs['placeholder'] = field.label


class ContactForm(SetFieldClassesMixin, forms.Form):
    email_address = forms.EmailField(label=_("Your e-mail address"))
    subject = forms.CharField(label=_("Subject of message"))
    body = forms.CharField(label=_("Message"), widget=forms.Textarea)

    def __init__(self, email=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if email:
            # we have an authenticated email address
            self.email = email
            del self.fields['email_address']


class ProductForm(forms.ModelForm):
    class Meta(object):
        model = Product

    def clean(self):
        if 'quantifiable' in self.cleaned_data and 'pricing' in self.cleaned_data:
            quantifiable = self.cleaned_data['quantifiable']
            pricing = self.cleaned_data['pricing']
            if pricing == Product.PRICE_USER and quantifiable:
                # Just force quantifiable
                self.cleaned_data['quantifiable'] = False
        return self.cleaned_data


class OrderLineForm(forms.ModelForm):

    class Meta(object):
        model = OrderLine
        fields = ['quantity', 'amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.prefix:
            if self.instance.price:
                self.prefix = '%s_%s' % (self.instance.product.pk, self.instance.price.pk)
            else:
                self.prefix = '%s' % (self.instance.product.pk, )
        if self.instance.product.pricing != Product.PRICE_USER:
            del self.fields['amount']
        if not self.instance.product.quantifiable:
            del self.fields['quantity']

    def has_any(self):
        if self.instance.product.pricing == Product.PRICE_USER:
            return self.cleaned_data['amount'] != Decimal('0.00')
        else:
            return self.cleaned_data['quantity'] != 0
