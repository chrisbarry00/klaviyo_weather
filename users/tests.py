from django.core.urlresolvers import reverse
from django.test import TestCase
from cities.models import City
from users.models import User


class UserTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(
            name="Boston",
            state="MA",
            order=1
        )

    def create_test_user(self):
        return User.objects.create(
            email='weather_test@example.com',
            city=self.city
        )

    def test_user_creation(self):
        user = self.create_test_user()
        self.assertTrue(isinstance(user, User))

    def test_user_signup_view(self):
        resp = self.client.get(reverse('users:signup'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'signup.html')
