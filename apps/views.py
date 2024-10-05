from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import ImageModel
from .serializers import ImageGETSerializers, ImageUploadSerializers


class ImageGETAPI(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageGETSerializers
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get"]


class CreateView(CreateAPIView):
    parser_class = [MultiPartParser, FormParser]
    serializer_class = ImageUploadSerializers
