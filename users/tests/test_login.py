from allauth.account.forms import LoginForm
# from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
import mock

# from store.forms import MemberLoginForm
#from store.utils import log_member_in


# class LoginUtilsTest(TestCase):
#     def test_not_logged_in(self):
#         request = Mock()
#         request.session = {}
#         self.assertFalse(member_is_logged_in(request))
#
#     def test_logged_in(self):
#         request = Mock()
#         request.session = {'member': True}
#         self.assertTrue(member_is_logged_in(request))
#
#     def test_log_member_in(self):
#         request = Mock(session={})
#         self.assertFalse(member_is_logged_in(request))
#         log_member_in(request)
#         self.assertTrue(member_is_logged_in(request))


class LoginTest(TestCase):
    def setUp(self):
        self.url = reverse('account_login') + '?next=' + reverse('store')

    def test_get(self):
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertTemplateUsed(rsp, 'account/login.html')
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, LoginForm))

    @override_settings(MEMBER_PASSWORD='password')
    @mock.patch('store.utils.log_member_in')
    def test_bad_pass(self, mock_log_member_in):
        data = {'password': 'not_password'}
        rsp = self.client.post(self.url, data=data)
        self.assertEqual(200, rsp.status_code)
        self.assertTemplateUsed(rsp, 'account/login.html')
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertTrue(form.errors)
        self.assertFalse(mock_log_member_in.called)
