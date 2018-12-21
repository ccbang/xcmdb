from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Host(models.Model):
    description = models.TextField()
    enabled = models.BooleanField()
    variables = JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    last_job = models.ForeignKey('Job', models.DO_NOTHING, blank=True, null=True)
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