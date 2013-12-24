"""
Test store views that aren't tested elsewhere
"""
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.timezone import now
import mock
from model_mommy import mommy
from store.models import ProductGroup, Product


class TestStoreView(TestCase):
    def setUp(self):
        self.url = reverse('store')
        self.member_url = reverse('member_view')
        self.public_group = ProductGroup.objects.create(
            display_start=now(),
            display_end=now() + timedelta(days=2),
            public=True,
            members=False
        )

    @mock.patch('store.views.member_is_logged_in')
    def test_member_not_logged_in(self, mock_member_is_logged_in):
        mock_member_is_logged_in.return_value = False
        rsp = self.client.get(self.member_url, follow=False)
        self.assertEqual(302, rsp.status_code)
        rsp = self.client.get(self.member_url, follow=True)
        self.assertEqual(200, rsp.status_code)
        self.assertRedirects(rsp,
                             reverse('member_login',
                                     kwargs=dict(next=reverse('member_view'))))

    @mock.patch('store.views.member_is_logged_in')
    def test_member_logged_in(self, mock_member_is_logged_in):
        mock_member_is_logged_in.return_value = True
        rsp = self.client.get(self.member_url, follow=False)
        self.assertEqual(200, rsp.status_code)

    def test_store(self):
        prod1 = mommy.make(Product, group=self.public_group)
        prod2 = mommy.make(Product, group=self.public_group)
        rsp = self.client.get(self.url)
        products = rsp.context['products']
        self.assertEqual(2, len(products))
