from django.db import models
from django.conf import settings


class Credentials(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='credentials',
        on_delete=models.CASCADE,
    )
    public = models.FileField(upload_to='credentials/')
    private = models.FileField(upload_to='credentials/')