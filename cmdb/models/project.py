from django.db import models
from django.conf import settings


class Member(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="members",
        on_delete=models.CASCADE
    )
    role = models.ForeignKey(
        'Role',
        related_name='members',
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'Project',
        related_name='members',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("project", 'role')


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ("name",)
