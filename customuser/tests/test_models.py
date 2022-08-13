from django.test import TestCase
from django.db import IntegrityError

from ..models import CustomUser


class CustomUserManagerTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='johndoe@email.com',
            first_name='John',
            last_name='Doe',
            password='password123',
        )

        self.superuser = CustomUser.objects.create_superuser(
            email='janedoe@email.com',
            first_name='Jane',
            last_name='Doe',
            password='password321',
        )

    def test_user_is_created_by_create_user_method(self):
        user_from_database = CustomUser.objects.get(email='johndoe@email.com')
        self.assertTrue(CustomUser.objects.filter(email='johndoe@email.com').exists())
        self.assertEqual(self.user.email, user_from_database.email)

    def test_user_created_is_not_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_superuser_is_created_by_create_superuser_method(self):
        superuser_from_database = CustomUser.objects.get(email='janedoe@email.com')
        self.assertTrue(CustomUser.objects.filter(email='janedoe@email.com').exists())
        self.assertEqual(self.superuser.email, superuser_from_database.email)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)

    def test_create_superuser_with_is_superuser_false_fails(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='adampeters@email.com',
                first_name='Adam',
                last_name='Peters',
                password='password456',
                is_superuser=False,
            )

    def test_create_superuser_with_is_staff_false_fails(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email='adampeters@email.com',
                first_name='Adam',
                last_name='Peters',
                password='password456',
                is_staff=False,
            )


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='johndoe@email.com',
            first_name='John',
            last_name='Doe',
            password='password123',
        )

    def test_user_email_is_unique(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
               email='johndoe@email.com',
            )

    def test_username_is_email(self):
        self.assertEqual(self.user.email, self.user.username)

    def test_str_method_is_returning_user_email(self):
        self.assertEqual(str(self.user), 'johndoe@email.com')
        self.assertEqual(self.user.__srt__(), 'johndoe@email.com')
