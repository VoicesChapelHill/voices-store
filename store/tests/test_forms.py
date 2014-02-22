from decimal import Decimal
from django.test import TestCase
from django.test.utils import override_settings
from model_mommy import mommy
from store.forms import MemberLoginForm, ContactForm, OrderLineForm
from store.models import Product, OrderLine, Price

PASSWORD = 'qwerty'
EMAIL = 'foo@example.com'
SUBJECT = 'contact!'
BODY = 'body\nbody2\n'


@override_settings(MEMBER_PASSWORD=PASSWORD)
class TestMemberLoginForm(TestCase):
    def test_good(self):
        data = {
            'password': PASSWORD
        }
        form = MemberLoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_bad(self):
        data = {
            'password': 'not ' + PASSWORD
        }
        form = MemberLoginForm(data=data)
        self.assertFalse(form.is_valid())


class TestContactForm(TestCase):
    def test_with_email(self):
        data = {
            'subject': SUBJECT,
            'body': BODY,
        }
        form = ContactForm(email=EMAIL, data=data)
        self.assertTrue(form.is_valid())
        out = form.cleaned_data
        self.assertEqual(EMAIL, out['email_address'])
        self.assertEqual(SUBJECT, out['subject'])
        self.assertEqual(BODY, out['body'])

    def test_without_email(self):
        data = {
            'email_address': EMAIL,
            'subject': SUBJECT,
            'body': BODY,
        }
        form = ContactForm(email=None, data=data)
        self.assertTrue(form.is_valid())
        out = form.cleaned_data
        self.assertEqual(EMAIL, out['email_address'])
        self.assertEqual(SUBJECT, out['subject'])
        self.assertEqual(BODY, out['body'])

    def test_without_subject(self):
        data = {
            'email_address': EMAIL,
            'subject': '',
            'body': BODY,
        }
        form = ContactForm(email=None, data=data)
        self.assertFalse(form.is_valid())

    def test_without_body(self):
        data = {
            'email_address': EMAIL,
            'subject': SUBJECT,
            'body': '',
        }
        form = ContactForm(email=None, data=data)
        self.assertFalse(form.is_valid())


class TestOrderLineForm(TestCase):
    def test_empty_unbound(self):
        TestOrderLineForm()

    def test_user_price_unbound(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_USER,
            quantifiable=False,
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        form = OrderLineForm(instance=line)
        self.assertIn('amount', form.fields)
        self.assertNotIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.prefix.startswith(product.slug))
        with self.assertRaises(ValueError):
            form.has_any()

    def test_one_price_unbound(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_ONE,
            quantifiable=True,
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        form = OrderLineForm(instance=line)
        self.assertNotIn('amount', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        with self.assertRaises(ValueError):
            form.has_any()

    def test_multi_price_unbound(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_MULTIPLE,
            quantifiable=True,
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        form = OrderLineForm(instance=line)
        self.assertNotIn('amount', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        with self.assertRaises(ValueError):
            form.has_any()

    def test_user_price_bound(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_USER,
            quantifiable=False,
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        tmp_form = OrderLineForm(instance=line)
        data = {
            tmp_form.add_prefix('amount'): '1.23',
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertIn('amount', form.fields)
        self.assertNotIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.prefix.startswith(product.slug))
        self.assertTrue(form.has_any())
        self.assertEqual(Decimal('1.23'), form.cleaned_data['amount'])

    def test_one_price_bound(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_ONE,
            quantifiable=True,
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        tmp_form = OrderLineForm(instance=line)
        data = {
            tmp_form.add_prefix('quantity'): 1,
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('amount', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.has_any())

    def test_special_instructions(self):
        product = mommy.prepare(
            Product,
            pricing=Product.PRICE_ONE,
            quantifiable=False,
            special_instructions_prompt='Enter your name',
        )
        line = mommy.prepare(
            OrderLine,
            product=product)
        tmp_form = OrderLineForm(instance=line)
        data = {
            tmp_form.add_prefix('quantity'): 1,
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertFalse(form.is_valid())
        data[tmp_form.add_prefix('special_instructions')] = 'foo'
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(data[tmp_form.add_prefix('special_instructions')],
                         form.cleaned_data['special_instructions'])

    def test_one_price_with_price(self):
        price = mommy.make(
            Price,
        )
        product = mommy.make(
            Product,
            prices=[price],
            pricing=Product.PRICE_ONE,
            quantifiable=True,
        )
        line = mommy.prepare(
            OrderLine,
            price=price,
            product=product)
        tmp_form = OrderLineForm(instance=line)
        self.assertTrue(tmp_form.prefix.startswith(product.slug))
        self.assertTrue(tmp_form.prefix.endswith(str(price.pk)))
        data = {
            tmp_form.add_prefix('quantity'): 1,
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('amount', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.has_any())

    def test_multi_price_with_price(self):
        price1 = mommy.make(
            Price,
        )
        price2 = mommy.make(
            Price,
        )
        product = mommy.make(
            Product,
            prices=[price1, price2],
            pricing=Product.PRICE_MULTIPLE,
            quantifiable=True,
        )
        line = mommy.prepare(
            OrderLine,
            product=product,
            price=price1)
        tmp_form = OrderLineForm(instance=line)
        self.assertEqual(tmp_form.prefix, '%s_%s' % (product.slug, price1.pk))
        data = {
            tmp_form.add_prefix('quantity'): 1,
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('amount', form.fields)
        self.assertIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.has_any())

    def test_unquantifiable_not_user_price(self):
        # E.g. member dues
        price = mommy.make(
            Price,
        )
        product = mommy.make(
            Product,
            prices=[price],
            pricing=Product.PRICE_ONE,
            quantifiable=False,
        )
        line = mommy.prepare(
            OrderLine,
            price=price,
            product=product)
        tmp_form = OrderLineForm(instance=line)
        self.assertTrue(tmp_form.prefix.startswith(product.slug))
        self.assertTrue(tmp_form.prefix.endswith(str(price.pk)))
        data = {
        }
        form = OrderLineForm(instance=line, data=data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('amount', form.fields)
        self.assertNotIn('quantity', form.fields)
        self.assertNotIn('special_instructions', form.fields)
        self.assertTrue(form.has_any())
