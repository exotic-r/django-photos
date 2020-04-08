from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField(upload_to='images/')
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.caption