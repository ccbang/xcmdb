from django.db import models


class Group(models.Model):
    group_name = models.CharField('组名称', max_length=100)
    pp_id = models.IntegerField('父组ID', default=0)


class Role(models.Model):
    group = models.ForeignKey(
        'Group',
        null=True,
        blank=True,
        related_name="roles",
        on_delete=models.SET_NULL
    )
    role_ame = models.CharField('角色名', max_length=100)
    desc = models.CharField('描述1', blank=True, max_length=100)
    permission = models.ManyToManyField('AuthPermission', blank=True)