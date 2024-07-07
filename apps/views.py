from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .models import ImageModel
from .serializers import ImageSerializers

class ImageCreateAPIView(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializers
    http_method_names = ["get","post","options"]