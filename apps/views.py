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
            images = []
            for image_data in request.FILES.getlist('image'):
                serializer = ImageSerializers(data={'image': image_data})
                if serializer.is_valid():
                    serializer.save()
                    images.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"images": images}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        images = ImageModel.objects.all()
        serializer = ImageSerializers(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)