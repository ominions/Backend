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

    def create(self, request, *args, **kwargs):
        serializer = ImageSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        images = ImageModel.objects.all()
        serializer = ImageSerializers(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
