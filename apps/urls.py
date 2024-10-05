from django.urls import include, path
from rest_framework import routers

from .views import CreateView, ImageGETAPI

router = routers.DefaultRouter()
router.register(r"images", ImageGETAPI, basename="images")
# router.register(r"upload", ImageCreateAPIView, basename="upload")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/upload/", CreateView.as_view(), name="image_upload"),
]
