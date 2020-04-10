from django.test import TestCase
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User

class UserSerializerTest(TestCase):

    def test_user_serializers(self):
        user = User.objects.create(**{
            'username':'sho',
            'password': 'shhhhhhhhh'
        })
        data = UserSerializer(instance=user).data
        # cannot read password
        self.assertEqual(set(data.keys()), set(['username', 'id']))