from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import  ContentType


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        unique_together = (('content_type', 'codename'),)
        ordering = ("codename", )

