# serializers.py
import pyrebase
from django.conf import settings
from rest_framework import serializers

from .models import ImageModel, JSONData, PlyData


class ImageGETSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"


class ImageUploadSerializers(serializers.ModelSerializer):
    # images = ImageGETSerializers(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
    )

    class Meta:
        model = ImageModel
        fields = ["uploaded_images"]

    def create(self, validate_date):
        uploaded_images = validate_date.pop("uploaded_images")
        firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
        storage = firebase.storage()
        image_urls = []
        # images = ImageModel.objects.create(**validate_date)

        for image in uploaded_images:
            # upload the image to firebase storage
            path_on_cloud = f"images/{image.name}"
            storage.child(path_on_cloud).put(image)

            # get url of uploaded images
            image_url = storage.child(path_on_cloud).get_url(None)
            image_urls.append(image_url)

            # save
            ImageModel.objects.create(image_url=image_url)

        return {"uploaded_images": image_urls}


class JSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = JSONData
        fields = ['id', 'data']

class PLYViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlyData
        fields = "__all__"


class PLYDataSerializer(serializers.ModelSerializer):
    uploaded_files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
    )
    
    class Meta:
        model = PlyData
        fields = ["uploaded_files"]

    def create(self, validated_data):
        uploaded_files = validated_data.pop("uploaded_files")
        
        # Initialize Firebase
        firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
        storage = firebase.storage()
        
        file_urls = []

        for file in uploaded_files:
            # Upload each .ply file to Firebase Storage
            path_on_cloud = f"ply_files/{file.name}"
            storage.child(path_on_cloud).put(file)
            
            # # Get the URL of the uploaded file
            file_url = storage.child(path_on_cloud).get_url(None)
            file_urls.append(file_url)

            # Save the PLYData instance with the file URL
            PlyData.objects.create(ply_file_url=file_url)

        # Return URLs of all uploaded files
        return {"uploaded_files": file_urls}