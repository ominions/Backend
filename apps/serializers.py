# serializers.py
from rest_framework import serializers
from .models import ImageModel

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"
