import datetime
import decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

import lunarphaseapp.views as lunarphase_views


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'my@email.com', 'password')
        self.client.login(username='user', password='password')

    def test_gets_lunar_phase_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phase Name")
        self.assertContains(response, "Rounded Position")

    def test_returns_the_correct_position(self):
        position = lunarphase_views.position(datetime.datetime(2020, 10, 10, 12, 10, 5))
        rounded_position = round(float(position), 3)
        self.assertEqual(rounded_position, 0.782)

    def test_returns_the_correct_phase(self):
        dec = decimal.Decimal
        phase_name = lunarphase_views.phase(dec(0.1002))
        self.assertEqual(phase_name, "Waxing Crescent")
