from django.urls import path, include

from rest_framework import routers

from .views import ImageCreateAPIView

router = routers.DefaultRouter()
router.register(r"images", ImageCreateAPIView, basename="images")

urlpatterns = [
    path("api/", include(router.urls)),
    # path('api/upload/', ImageCreateAPIView.as_view(),name="image_upload"),
]
