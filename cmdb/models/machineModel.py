from django.db import models
from .xroleModel import Roles
from django.contrib.postgres.fields import ArrayField, JSONField


class Machines(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL)
    mac_address = models.CharField("MAC地址", max_length=255)
    machine_ip = JSONField('IP信息', default=dict)
    status = models.CharField('机器状态', max_length=10, blank=True)
    memory = models.IntegerField('内存bytes', default=0)
    virtual_cpu = models.IntegerField('CPU核数', default=0)
    disk = models.IntegerField('硬盘大小bytes', default=0)
