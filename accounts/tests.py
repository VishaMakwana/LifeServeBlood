from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.test import override_settings
from django.contrib.auth.models import User

from donor.models import Donor
from patient.models import Patient
from accounts.models import UserProfile


class AccountFlowTests(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_register_redirects_directly_to_login(self):
        response = self.client.post(
            reverse('register'),
            {
                'fullname': 'Sam',
                'username': 'sam123',
                'email': 'sam@example.com',
                'phone': '9876543210',
                'age': '25',
                'gender': 'Male',
                'blood_group': 'O+',
                'city': 'Ahmedabad',
                'address': 'Test address',
                'state': 'Gujarat',
                'password': 'StrongPass123',
                'confirm_password': 'StrongPass123',
                'role': 'Donor',
            },
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        self.assertTrue(User.objects.filter(username='sam123').exists())
        self.assertTrue(Donor.objects.filter(user__username='sam123').exists())
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_donor_login_requires_login_otp(self):
        user = User.objects.create_user(
            username='donoruser',
            first_name='Donor',
            email='donor@example.com',
            password='StrongPass123',
        )
        UserProfile.objects.create(user=user, phone='9999999999', role='Donor')
        Donor.objects.create(
            user=user,
            age=28,
            gender='Male',
            blood_group='A+',
            city='Ahmedabad',
            state='Gujarat',
            address='Donor address',
        )

        response = self.client.post(
            reverse('login'),
            {'username': 'donoruser', 'password': 'StrongPass123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('verify_login_otp'))
        self.assertEqual(len(mail.outbox), 1)
