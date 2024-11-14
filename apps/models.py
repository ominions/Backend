from django.db import models


class ImageModel(models.Model):
    image = models.ImageField(upload_to="images/")
    image_url = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"

class JSONData(models.Model):
    data = models.JSONField()

    def __str__(self):
        return f"JSON Data Id: {self.id}"


class PlyData(models.Model):
    ply_file = models.FileField(upload_to="ply_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
