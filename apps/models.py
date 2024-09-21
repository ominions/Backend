from django.db import models


class ImageModel(models.Model):
    image = models.ImageField(upload_to="images/")
    image_url = models.URLField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
