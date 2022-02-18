from django.conf import settings
from django.db import models
from django.utils import timezone


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(
        blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image_url = models.URLField(
        max_length=1024, null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
