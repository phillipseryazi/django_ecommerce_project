from django.test import TestCase, RequestFactory, Client
from .models import User
from .views import RegistrationView
from .forms import RegistrationForm


# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = {
            'username': 'username',
            'email': 'email',
            'phone': 'phone',
            'password': 'password'
        }

    def test_create_user(self):
        user = User.objects.create_user(username='username', email='user@gmail.com',
                                        phone='256000000000', bio='i am a user',
                                        image='www.image.com', password='password')
        self.assertEqual(user.email, 'user@gmail.com')

    def test_registration_form(self):
        request = self.factory.get('sellex/v1/auth/register/')
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        form = RegistrationForm(self.user)
        request = self.factory.post('sellex/v1/auth/register/', data=form,
                                    content_type='application/x-www-form-urlencoded')
        response = RegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
