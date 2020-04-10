from django.test import TestCase
from photos.serializers import PhotoListSerializer, PhotoSerializer
from photos.models import Photo
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class PhotoSerializerTest(TestCase):

    def setUp(self):
        # save a user & get/set access token 
        self.user = User.objects.create_user(
            username='sho',password='shhhhhhhhh'
        )

    def test_photo_serializers(self):
        photo = Photo.objects.create(**{
            'author' : self.user,
            'caption' : 'an image',
            'image' : SimpleUploadedFile(
                name='test_image.jpg', 
                content=open('photos/tests/test_image.jpg', 'rb').read(), 
                content_type='image/jpeg'
            ),
        })

        data = PhotoSerializer(instance=photo).data
        self.assertEqual(set(data.keys()), set(['id', 'image', 'created', 'author', 'caption', 'draft']))