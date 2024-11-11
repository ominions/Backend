from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImageModel, JSONData, PlyData
from .serializers import ImageGETSerializers, ImageUploadSerializers, JSONSerializer, PLYDataSerializer


class ImageGETAPI(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageGETSerializers
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get"]


class CreateView(CreateAPIView):
    parser_class = [MultiPartParser, FormParser]
    serializer_class = ImageUploadSerializers

class JSONUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JSONSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JSONRetriveView(APIView):
    def get(self, request, id=None, *args, **kwargs):
        try:
            if id:
                json_data = JSONData.objects.get(id=id)
                serializer = JSONSerializer(json_data)
            else:
                json_data = JSONData.objects.all()
                serializer = JSONSerializer(json_data, many=True)

            return Response(serializer.data, status = status.HTTP_200_OK)
        except JSONData.DoesNotExist:
            return Response({"Error": "Data not Found"}, status=status.HTTP_400_NOT_FOUND)

class PLYUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PLYDataSerializer(data = request.data)
        if serializer.is_valid():
            file_urls=serializer.save()
            return Response(file_urls, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlyGetAPI(viewsets.ModelViewSet):
    queryset = PlyData.objects.all()
    serializer_class = PLYDataSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get"]