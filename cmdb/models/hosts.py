from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

SU = 'success'
PR = "processing"
DE = "default"
ER = "error"
WA = "warning"

STATUS_CHOICES = (
    (SU, '已上线'),
    (PR, '运行中'),
    (DE, '未分配'),
    (ER, '异常'),
    (WA, '警告'),
)


class Host(models.Model):
    project = models.ManyToManyField(
        'Project',
        related_name='hosts',
        blank=True,
    )
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DE)
    enabled = models.BooleanField(default=True)
    variables = JSONField(default=dict)
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
    cpu = models.IntegerField()
    memory = models.BigIntegerField(default=0)
    cpu_capacity = models.IntegerField(default=0)
    mem_capacity = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created', 'hostname')
