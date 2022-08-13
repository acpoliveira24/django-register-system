from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from customuser.models import CustomUser


class CustomUserIndexViewTestCase(TestCase):
    def test_index_view_status_is_ok(self):
        response = self.client.get(reverse('customuser:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class CustomUserSignupViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'johndoe123',
            'confirm_password': 'johndoe123'
        }

        self.data_not_valid = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'johndoe123',
            'confirm_password': ''
        }

        self.signup_url = reverse('customuser:signup')
        self.index_url = reverse('customuser:index')

    def test_signup_view_form_is_valid_and_redirects_to_index(self):
        response = self.client.post(
            self.signup_url,
            data=self.data,
            follow=True
        )

        self.assertRedirects(response, self.index_url, status_code=302)

    def test_signup_view_form_is_not_valid(self):
        response = self.client.post(
            self.signup_url,
            data=self.data_not_valid,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_signup_view_request_is_not_post(self):
        response = self.client.get(
            self.signup_url,
            data=self.data_not_valid,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class CustomUserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='johndoe@email.com',
            first_name='John',
            last_name='Doe',
            password='johndoe123'
        )

        self.login_url = reverse('customuser:login')
        self.index_url = reverse('customuser:index')

    def test_login_view_form_is_valid_and_user_can_login(self):
        response = self.client.post(
            self.login_url,
            data={
                'email': 'johndoe@email.com',
                'password': 'johndoe123'
            },
            follow=True
        )

        user_is_authenticated = self.client.login(
            email='johndoe@email.com',
            password='johndoe123'
        )

        self.assertRedirects(response, self.index_url, status_code=302)
        self.assertTrue(user_is_authenticated)

    def test_login_view_user_does_not_exist(self):
        response = self.client.post(
            self.login_url,
            data={
                'email': 'otherjohn@email.com',
                'password': 'password123'
            },
            follow=True
        )

        user_is_authenticated = self.client.login(
            email='otherjohn@email.com',
            password='password123'
        )

        all_messages = [msg for msg in get_messages(response.wsgi_request)]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_is_authenticated)
        self.assertEqual(all_messages[0].message, 'User with this e-mail does not exist')

    def test_login_view_with_invalid_password(self):
        response = self.client.post(
            self.login_url,
            data={
                'email': 'johndoe@email.com',
                'password': 'password123'
            },
            follow=True
        )

        user_is_authenticated = self.client.login(
            email='johndoe@email.com',
            password='password123'
        )

        all_messages = [msg for msg in get_messages(response.wsgi_request)]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user_is_authenticated)
        self.assertEqual(all_messages[0].message, 'Invalid Password')

    def test_login_view_form_is_not_valid(self):
        response = self.client.post(
            self.login_url,
            data={
                'email': 'abc',
                'password': ''
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_login_view_request_is_not_post(self):
        response = self.client.get(
            self.login_url,
            data={
                'email': 'abc',
                'password': ''
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class CustomUserLogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='johndoe@email.com',
            first_name='John',
            last_name='Doe',
            password='johndoe123'
        )

        self.login_url = reverse('customuser:login')
        self.logout_url = reverse('customuser:logout')
        self.index_url = reverse('customuser:index')

    def test_logout_view_user_can_logout(self):
        self.client.post(
            self.login_url,
            data={
                'email': 'johndoe@email.com',
                'password': 'johndoe123'
            },
            follow=True
        )

        user_is_authenticated = self.client.login(
            email='johndoe@email.com',
            password='johndoe123'
        )

        response = self.client.get(self.logout_url)

        user_is_authenticated= self.client.logout()

        self.assertRedirects(response, self.index_url, status_code=302)
        self.assertFalse(user_is_authenticated)
