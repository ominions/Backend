# serializers.py
from rest_framework import serializers
from .models import ImageModel

class ImageSerializers(serializers.ModelSerializer):
    image = serializers.FileField(required=False, write_only=True)
    image_url = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = ImageModel
        fields = "__all__"

    def create(self, validated_data):
        #Check if 'image' or 'image_url' is provided
        image = validated_data.pop('image', None)
        image_url = validated_data.pop('image_url', None)

        if image:
            instance = super().create(validated_data)
            instance.image = image
            instance.save()
            return instance
        elif image_url:
            #handling image url processing here
            instance = super().create(validated_data)
            instance.image_url = image_url
            instance.save()
            return instance
        else:
            return serializers.ValidationError("Either 'image' or 'image_url' must be provided.")