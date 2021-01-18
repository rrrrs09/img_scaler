from django.db import models
from django.urls import reverse


class UploadedImage(models.Model):
    img = models.ImageField()

    def __str__(self):
        return self.img.name

    def get_absolute_url(self):
        return reverse('detail', args=[self.pk])
