from django.db import models
from django.contrib.auth.models import Permission


class RoleGroup(models.Model):
    group_name = models.CharField('组名称', max_length=100)
    pp_id = models.IntegerField('父组ID', default=0)


class Role(models.Model):
    group = models.ForeignKey(
        'RoleGroup',
        null=True,
        blank=True,
        related_name="roles",
        on_delete=models.SET_NULL
    )
    name = models.CharField('角色名', max_length=100)
    desc = models.CharField('描述1', blank=True, max_length=100)
    permission = models.ManyToManyField(Permission, blank=True)

    class Meta:
        ordering = ("name", )