from django.urls import reverse
from photos.models import Photo
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from photos.views import PhotoView
from django.core.files.uploadedfile import SimpleUploadedFile
import time

class PhotoViewTest(APITestCase):

    def assert_respose(self, response, expected_caption, isDraft):
        self.assertEquals(response.get('caption'), expected_caption)
        self.assertEquals(response.get('draft'), isDraft)
        self.assertEquals(response.get('author'), 1)

    def post_photo(self, isDraft=False):
        data = {
            'caption' : 'an image',
            'image' : SimpleUploadedFile(
                name='test_image.jpg', 
                content=open('photos/tests/test_image.jpg', 'rb').read(), 
                content_type='image/jpeg'
            ),
            'draft' : isDraft,
        }
        response = self.client.post('/photos/', data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        # save a user & get/set access token 
        User.objects.create_user(
            username='sho',password='shhhhhhhhh'
        ).save()

        data = {'username':'sho','password':'shhhhhhhhh'}
        url = reverse('token_create')

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
    
    def tearDown(self):
        import shutil
        try:
            shutil.rmtree('media/images')
        except OSError:
            pass

    def test_get_empty_photo_list(self):
        response = self.client.get('/photos/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Photo.objects.count(), 0)

    def test_get_photo_list(self):
        self.post_photo()

        response = self.client.get('/photos/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)
        response_data = response.data[0]
        self.assert_respose(response_data, 'an image', False)

    def test_single_photo(self):
        self.post_photo()

        response = self.client.get('/photos/1/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 6)
        self.assert_respose(response.data, 'an image', False)

    def test_update_caption(self):
        self.post_photo()
        data = {
            'caption' : 'changed caption'
        }
        response = self.client.patch('/photos/1/', data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_my_photo(self):
        self.post_photo()

        response = self.client.get('/photos/my_photos/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

        response_data = response.data[0]
        self.assert_respose(response_data, 'an image', False)

    def test_get_my_draft_photo(self):
        self.post_photo(isDraft=True)

        response = self.client.get('/photos/my_drafts/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)     

    def test_delete_photo(self):
        self.post_photo()
                
        response = self.client.delete('/photos/1/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_order_photo(self):
        self.post_photo()
        time.sleep(0.1)
        self.post_photo()

        # ASC
        response = self.client.get('/photos/?ordering=created')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        p1 = response.data[0].get('created')
        p2 = response.data[1].get('created')
        self.assertTrue(p1 < p2)

        # DESC
        response = self.client.get('/photos/?ordering=-created')
        
        p1 = response.data[0].get('created')
        p2 = response.data[1].get('created')
        self.assertTrue(p1 > p2)

    def test_filter_photo_by_user(self):
        self.post_photo()

        User.objects.create_user(
            username='Naruto',password='ninjaaaaaaa'
        ).save()

        response = self.client.get('/photos/?author=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 1)      

        response = self.client.get('/photos/?author=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(len(response.data), 0)                  