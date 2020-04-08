from rest_framework import serializers
from .models import Photo
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .const import MAX_WIDTH, MAX_HEIGHT, MEGA_BYTE_LIMIT

def validated_size(self):
    image_byte = self.size
    if image_byte > MEGA_BYTE_LIMIT*1024*1024:
        raise ValidationError("Maximum image size is {} MB".format(MEGA_BYTE_LIMIT))

def validated_dimensions(self):
    width, height = get_image_dimensions(self)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        errors = []
        errors.append('Photo (width,height)=({},{}), should be > ({},{}) px'.format(
            width, height,
            MAX_WIDTH, MAX_HEIGHT
        ))
        raise ValidationError(errors)


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validated_size, validated_dimensions])
    
    class Meta:
        model = Photo
        fields = ('id', 'author', 'caption', 'draft', 'image', 'created')


class PhotoListSerializer(serializers.ListSerializer):
    child = PhotoSerializer()
    many = True



