from django.db import models
from django.contrib.postgres.fields import JSONField

TODO = 'todo'
PROCESSING = 'processing'
URGENT = 'urgent'
DOING = 'doing'
STATUS_CHOICES = (
    (TODO, '完成'),
    (PROCESSING, '进行中'),
    (URGENT, '优先操作'),
    (DOING, '操作中')
)


class Job(models.Model):
    name = models.CharField(max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)
    done_time = models.DateTimeField()
    playbook = JSONField()


class JobHost(models.Model):
    host = models.ForeignKey("Host", related_name='jobs', on_delete=models.SET_NULL, null=True, blank=True)
    result = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
