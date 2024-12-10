from django.shortcuts import render
# from django.http import StreamingHttpResponse
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_date


from .models import ImageModel, JSONData, PlyData
from .serializers import ImageGETSerializers, ImageUploadSerializers, JSONSerializer, PLYDataSerializer, PLYViewSerializer

import pyrebase
from django.conf import settings

class ImageGETAPI(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageGETSerializers
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get("date")

        if date:
            parsed_date = parse_date(date)
            if not parsed_date:
                raise ValidationError({"date": "Invalid date format. Use 'YYYY-MM-DD'."})

            # Filter by uploaded_at date
            queryset = queryset.filter(uploaded_at__date=parsed_date)

        return queryset


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


class PLYListView(APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        # Fetch all PlyData objects from the database
        ply_data = PlyData.objects.all()

        if 'date' in query_params:
            date = parse_date(query_params['date'])
            ply_data = ply_data.filter(uploaded_at__date=date)

        # Serialize the data
        serializer = PLYViewSerializer(ply_data, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)