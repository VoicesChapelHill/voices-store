from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from store.forms import MemberLoginForm


class LoginTest(TestCase):
    def setUp(self):
        self.url = reverse('member_login', kwargs=dict(next=reverse('store')))

    def test_get(self):
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, MemberLoginForm))

    @override_settings(MEMBER_PASSWORD='password')
    def test_bad_pass(self):
        data = {'password': 'not_password'}
        rsp = self.client.post(self.url, data=data)
        self.assertEqual(200, rsp.status_code)
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, MemberLoginForm))
        self.assertTrue(form.errors)

    @override_settings(MEMBER_PASSWORD='password')
    def test_good_pass(self):
        data = {'password': 'password'}
        rsp = self.client.post(self.url, data=data, follow=False)
        self.assertEqual(302, rsp.status_code)
        session = Session.objects.get()
        data = session.get_decoded()
        self.assertTrue(data['member'])
        self.assertRedirects(rsp, reverse('store'))
