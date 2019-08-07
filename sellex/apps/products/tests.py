import base64
from io import BytesIO

from unittest.mock import patch
from django.test import TestCase, Client, RequestFactory
from django.core.files.uploadedfile import InMemoryUploadedFile

from ..users.models import User
from ...utils.sample_image import TEST_IMAGE


# Create your tests here.
class ProductsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='username', email='user@gmail.com', password='password',
                                             phone='256000000000')
        self.client.login(username='user@gmail.com', password='password')

    def get_sample_image(self):
        image = InMemoryUploadedFile(
            BytesIO(base64.b64decode(TEST_IMAGE)),  # use io.BytesIO
            field_name='tempfile',
            name='tempfile.png',
            content_type='image/png',
            size=len(TEST_IMAGE),
            charset='utf-8',
        )
        return image

    def test_add_product_form(self):
        response = self.client.get('/sellex/v1/products/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    @patch('cloudinary.uploader.upload')
    def test_add_product(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        response = self.client.post('/sellex/v1/products/manage/',
                                    data={'name': 'product', 'details': 'product details',
                                          'price': '100000', 'image': image})
        self.assertEqual(response.status_code, 302)

    @patch('cloudinary.uploader.upload')
    def test_show_form_on_add_fail(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        response = self.client.post('/sellex/v1/products/manage/',
                                    data={'name': 'product', 'price': '100000', 'image': image})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/add_product.html')

    @patch('cloudinary.uploader.upload')
    def test_my_products_listview(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        self.client.post('/sellex/v1/products/manage/', data={'name': 'product', 'details': 'product details',
                                                              'price': '100000', 'image': image})
        self.client.post('/sellex/v1/products/update/1',
                         data={'name': 'updated product', 'details': 'updated product details',
                               'price': '100001'})
        response = self.client.get('/sellex/v1/products/myproducts/')
        self.assertEqual(response.status_code, 200)

    @patch('cloudinary.uploader.upload')
    def test_products_home(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        self.client.post('/sellex/v1/products/manage/', data={'name': 'product', 'details': 'product details',
                                                              'price': '100000', 'image': image})
        self.client.post('/sellex/v1/products/update/1',
                         data={'name': 'updated product', 'details': 'updated product details',
                               'price': '100001'})
        response = self.client.get('/sellex/v1/products/home/')
        self.assertEqual(response.status_code, 200)

    @patch('cloudinary.uploader.upload')
    def test_product_details(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        self.client.post('/sellex/v1/products/manage/', data={'name': 'product', 'details': 'product details',
                                                              'price': '100000', 'image': image})
        response = self.client.get('/sellex/v1/products/details/1/')
        self.assertEqual(response.status_code, 200)

    @patch('cloudinary.uploader.upload')
    def test_product_seach(self, cloudinary_obj):
        cloudinary_obj.return_value = {'url': 'http://www.google.com'}
        image = self.get_sample_image()
        self.client.post('/sellex/v1/products/manage/', data={'name': 'product', 'details': 'product details',
                                                              'price': '100000', 'image': image})
        response = self.client.get('/sellex/v1/products/search/', data={'search': 'product'})
        self.assertEqual(response.status_code, 200)
