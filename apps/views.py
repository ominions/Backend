from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import CreateAPIView

from .models import ImageModel
from .serializers import ImageGETSerializers,ImageUploadSerializers

class ImageGETAPI(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageGETSerializers
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get"]

class CreateView(CreateAPIView):
    parser_class = [MultiPartParser, FormParser]
    serializer_class = ImageUploadSerializers

# class ImageCreateAPIView(viewsets.ModelViewSet):
#     queryset = ImageModel.objects.all()
#     serializer_class = ImageSerializers
#     parser_classes = [MultiPartParser, FormParser]
#     http_method_names = ["post", "options"]

#     def create(self, request, *args, **kwargs):
#         serializer = ImageSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def list(self, request, *args, **kwargs):
#         images = ImageModel.objects.all()
#         serializer = ImageSerializers(images, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
