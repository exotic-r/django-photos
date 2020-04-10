from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from accounts.views import UserCreate


class RegisterationTest(APITestCase):
    def test_registeration(self):
        data = {'username':'sho','password':'shhhhhhhhh'}
        url = reverse('create_user')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'sho')


class TokenTest(APITestCase):

    def setUp(self):
        User.objects.create_user(
            username='sho',password='shhhhhhhhh'
        ).save()

    def test_create_refresh_token(self):
        data = {'username':'sho','password':'shhhhhhhhh'}
        url = reverse('token_create')
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('refresh')
        self.assertIsNotNone(token)

        data = {'refresh': token}
        url = reverse('token_refresh')
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))