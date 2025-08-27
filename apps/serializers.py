 # serializers.py
import pyrebase
from django.conf import settings
from rest_framework import serializers

from .models import (
    ImageModel,
    JSONData,
    PlyData
    )
from pathlib import Path
import requests
from .ply.generate_point_cloud import generate_point_cloud
from PIL import Image
from io import BytesIO
import subprocess

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
        image_ids = []
        # ImageModel.objects.all().delete()

        for image in uploaded_images:
            # upload the image to firebase storage
            path_on_cloud = f"images/{image.name}"  
            storage.child(path_on_cloud).put(image)

            # get url of uploaded images
            image_url = storage.child(path_on_cloud).get_url(None)
            image_urls.append(image_url)

            # save
            ImageModel.objects.create(image_url=image_url)
        self.download_images_from_urls(image_urls)

        return {"uploaded_images": image_urls}


    def download_images_from_urls(self, image_urls):
        # Firebase initialization
        firebase = pyrebase.initialize_app(settings.FIREBASE_CONFIG)
        storage = firebase.storage()

        # Temporary local directory for downloading images (Firebase does not support direct input for scripts)
        temp_folder = Path("/tmp/laptop_images")
        temp_folder.mkdir(parents=True, exist_ok=True)

        downloaded_files = []

        # Step 1: Download images from Firebase
        for url in image_urls:
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    # Save image temporarily
                    filename = temp_folder / Path(url).name
                    with open(filename, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    downloaded_files.append(filename)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download {url}. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        # Step 2: Run external Python script for point cloud generation
        self.create_point_cloud(temp_folder, storage)


    def create_point_cloud(self, input_folder, storage):
        try:
            output_folder = Path("/tmp/point_cloud_outputs")
            output_folder.mkdir(parents=True, exist_ok=True)
            ply_file_path = output_folder / "point_cloud.ply"

            # Run the generate_point_cloud script
            generate_point_cloud(input_folder, output_folder)
            # subprocess.run(
            #     ["python3", "./ply/generate_point_cloud.py", str(input_folder), str(output_folder)],
            #     check=True,
            # )

            # Check if the .ply file was generated
            if ply_file_path.exists():
                firebase_path = f"ply_files/points.ply"
                with open(ply_file_path, "rb") as ply_file:
                    storage.child(firebase_path).put(ply_file)
                print(f"Uploaded point cloud to Firebase: {firebase_path}")

                self.upload_ply_to_api(ply_file_path)
            else:
                print("Point cloud generation failed: .ply file not found.")
        except subprocess.CalledProcessError as e:
            print(f"Error running point cloud generation script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")



    def upload_ply_to_api(self, ply_file_path):
        """
        Upload the `.ply` file to the `/api/ply/upload` endpoint.
        """
        uploaded_url = "<url_api>"
        PlyData.objects.all().delete()
        try:
            with open(ply_file_path, 'rb') as ply_file:
                files = {
                    'uploaded_files': (
                        f"points.ply",
                        ply_file,
                        'application/octet-stream'
                    )
                }
                response = requests.post(uploaded_url, files=files)

            if response.status_code == 201:
                print("Successfully uploaded `.ply` file to API.")
            else:
                print(f"Failed to upload `.ply` file to API. Status Code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error uploading `.ply` file to API: {e}")




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
            try:
                # Upload each .ply file to Firebase Storage
                path_on_cloud = f"ply_files/{file.name}"
                storage.child(path_on_cloud).put(file)
                
                # Get the URL of the uploaded file
                file_url = storage.child(path_on_cloud).get_url(None)
                file_urls.append(file_url)

                # Save the PLYData instance with the file URL
                PlyData.objects.create(ply_file_url=file_url)
            except Exception as e:
                print(f"Error uploading {file.name}: {e}")
                raise serializers.ValidationError(f"Error uploading file {file.name}: {str(e)}")


        # Return URLs of all uploaded files
        return {"uploaded_files": file_urls}