 # serializers.py
import pyrebase
from django.conf import settings
from rest_framework import serializers

from .models import ImageModel, JSONData, PlyData
from pathlib import Path
import requests
from .ply.generate_point_cloud import generate_point_cloud

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
        self.download_images_from_urls(image_urls)

        return {"uploaded_images": image_urls}

    def download_images_from_urls(self, image_urls):
        project_folder = Path(__file__).resolve().parent.parent
        download_path = project_folder / "apps" / "ply" / "laptop_images"
        download_path.mkdir(parents=True, exist_ok=True)

        for url in image_urls:
            try:
                filename = download_path / Path(url).name
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(filename, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    
                    with Image.open(filename) as img:
                        png_filename = download_path / (filename.stem + '.png')
                        img.save(png_filename, 'PNG')
                        
                    print(f"Downloaded: {png_filename}")
                else:
                    print(f"Failed to download {url}. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        # Assuming `generate_point_cloud.py` is located at the same project level
        output_path = project_folder / "apps" / "ply" / "output"
        generate_point_cloud(download_path, output_path)

        file_path = project_folder / "apps" / "ply" / "point_cloud.ply"
        uploaded_url = 'http://127.0.0.1:8000/api/ply/upload/'

        with open(file_path, 'rb') as ply_file:
            files = {'uploaded_files': (f"points{ImageModel.objects.order_by('-id').values_list('id', flat=True).first()}.ply", ply_file, 'application/octet-stream')}
            response = requests.post(uploaded_url, files=files)

        print(response.status_code)  # 200 for success, or error details
        print(response.json())  # Response from the API



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