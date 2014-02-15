from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from mock import Mock
import mock

from store.forms import MemberLoginForm
from store.utils import log_member_in


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
        self.url = reverse('member_login', kwargs=dict(next=reverse('store')))

    def test_get(self):
        rsp = self.client.get(self.url)
        self.assertEqual(200, rsp.status_code)
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, MemberLoginForm))

    @override_settings(MEMBER_PASSWORD='password')
    @mock.patch('store.utils.log_member_in')
    def test_bad_pass(self, mock_log_member_in):
        data = {'password': 'not_password'}
        rsp = self.client.post(self.url, data=data)
        self.assertEqual(200, rsp.status_code)
        self.assertIn('form', rsp.context)
        form = rsp.context['form']
        self.assertTrue(isinstance(form, MemberLoginForm))
        self.assertTrue(form.errors)
        self.assertFalse(mock_log_member_in.called)

    @override_settings(MEMBER_PASSWORD='password')
    @mock.patch('store.utils.log_member_in')
    def test_good_pass(self, mock_log_member_in):
        data = {'password': 'password'}
        rsp = self.client.post(self.url, data=data, follow=False)
        self.assertEqual(302, rsp.status_code)
        session = Session.objects.get()
        data = session.get_decoded()
        self.assertTrue(data['member'])
        self.assertRedirects(rsp, reverse('store'))
        mock_log_member_in.assert_called()
