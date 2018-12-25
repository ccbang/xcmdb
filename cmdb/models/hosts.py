from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Host(models.Model):
    project = models.ManyToManyField(
        'Project',
        related_name='hosts',
        blank=True,
    )
    description = models.TextField()
    enabled = models.BooleanField()
    variables = JSONField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="create_hosts"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='modify_hosts'
    )
    last_job = models.ForeignKey(
        'Job',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='hosts'
    )
    uuid = models.CharField(max_length=40)
    hostname = models.CharField(unique=True, max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    capacity = models.IntegerField(default=0)
    version = models.CharField(max_length=24)
    last_isolated_check = models.DateTimeField(blank=True, null=True)
    capacity_adjustment = models.DecimalField(max_digits=3, decimal_places=2)
    cpu = models.IntegerField()
    memory = models.BigIntegerField()
    cpu_capacity = models.IntegerField()
    mem_capacity = models.IntegerField()
    managed_by_policy = models.BooleanField()