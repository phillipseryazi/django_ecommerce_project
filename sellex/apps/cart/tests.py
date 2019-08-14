import base64
from io import BytesIO
from unittest.mock import patch

from django.test import TestCase, Client, RequestFactory
from ..users.models import User
from ...utils.sample_image import TEST_IMAGE
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your tests here.
class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='username', email='user@gmail.com', password='password',
                                             phone='256000000000')
        self.client.login(username='user@gmail.com', password='password')
        self.add_product()

    def get_sample_image(self):
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        return image

    @patch('cloudinary.uploader.upload')
    def add_product(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        self.client.post('/sellex/v1/products/manage/', data={'name': 'product', 'details': 'product details',
                                                              'price': '100000', 'image': image})

    def test_add_to_cart(self):
        response = self.client.get('/sellex/v1/cart/add/1/1')
        self.assertEqual(response.status_code, 301)

    def test_get_cart(self):
        response = self.client.get('/sellex/v1/cart/get/')
        self.assertEqual(response.status_code, 200)
