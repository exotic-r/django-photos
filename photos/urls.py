from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from .views import PhotoView, UserView

router = routers.DefaultRouter()
router.register('photos', PhotoView)
router.register('user', UserView)

urlpatterns = [
    path('', include(router.urls)),
] 

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)