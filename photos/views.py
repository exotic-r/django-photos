from rest_framework import viewsets
from .models import Photo
from .serializers import PhotoSerializer
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer


class PhotoView(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['draft', 'author']
    ordering_fields = ['created']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=False)
    def my_photos(self, request):
        user = self.request.user
        my_photos = [ photo for photo in self.get_queryset() if photo.author == user ]
        serializer = PhotoSerializer(my_photos, many=True)
        
        return Response(serializer.data) 

    @action(methods=['get'], detail=False)
    def my_drafts(self, request):
        user = self.request.user
        my_draft_photos = [ photo for photo in self.get_queryset() if photo.author == user and photo.draft ]
        serializer = PhotoSerializer(my_draft_photos, many=True)
        
        return Response(serializer.data)         


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   
    filter_backends = [DjangoFilterBackend, OrderingFilter]       
    filter_fields = ['username']
    