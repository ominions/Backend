from django.urls import include, path
from rest_framework import routers

from .views import CreateView, ImageGETAPI, JSONUploadView, JSONRetriveView

router = routers.DefaultRouter()
router.register(r"images", ImageGETAPI, basename="images")
# router.register(r"upload", ImageCreateAPIView, basename="upload")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/upload/", CreateView.as_view(), name="image_upload"),
    path("api/cnn/", JSONUploadView.as_view(), name="upload_json"),
    path('api/cnn/jsondata/', JSONRetriveView.as_view(), name='get-all-json'),
    path('api/cnn/jsondata/<int:id>/', JSONRetriveView.as_view(), name='get-json-by-id'),
]
