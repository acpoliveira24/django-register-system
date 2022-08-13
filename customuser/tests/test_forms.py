from django.test import TestCase

from customuser.forms import CustomUserSignUpForm, CustomUserLoginForm
from customuser.models import CustomUser


class CustomUserSignUpFormTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'johndoe123',
            'confirm_password': 'johndoe123'
        }
        self.form = CustomUserSignUpForm(self.data)

    def test_init_method_is_setting_correct_css_class_for_fields_in_signup_form(self):
        for field_name, field in self.form.fields.items():
            css_class = field.widget.attrs['class']
            self.assertEqual(css_class, 'form-control')

    def test_save_method_is_saving_email_as_username(self):
        self.form.save()
        user = CustomUser.objects.get(email=self.data['email'])
        self.assertEqual(user.username, self.data['email'])

    def test_save_method_commit_false_not_saving(self):
        self.form.save(commit=False)
        with self.assertRaises(CustomUser.DoesNotExist):
            user = CustomUser.objects.get(email=self.data['email'])
            self.assertIsNone(user)

    def test_clean_email_method_returns_user_email_already_exists(self):
        CustomUser.objects.create_user(email='johndoe@email.com')
        self.assertFalse(self.form.is_valid())

    def test_password_and_confirm_password_is_not_the_same(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@email.com',
            'password': 'johndoe123',
            'confirm_password': 'johndoe456'
        }
        form = CustomUserSignUpForm(data)
        self.assertFalse(form.is_valid())


class CustomUserLoginFormTestCase(TestCase):
    def test_init_method_is_setting_correct_css_class_for_fields_in_login_form(self):
        data = {
            'email': 'johndoe@email.com',
            'password': 'johndoe123',
        }
        form = CustomUserLoginForm(data)
        for field_name, field in form.fields.items():
            css_class = field.widget.attrs['class']
            self.assertEqual(css_class, 'form-control')
