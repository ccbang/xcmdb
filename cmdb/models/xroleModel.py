from django.db import models


class UserGroup(models.Model):
    group_name = models.CharField('组名称', max_length=100)
    pp_id = models.IntegerField('父组ID', default=0)


class Users(models.Model):
    user_name = models.CharField('用户名称', max_length=200)
    position = models.CharField('职位', blank=True)
    api_key = models.CharField('API接口密钥', blank=True)
    ssh_pub = models.TextField('SSH公钥', blank=True)


class Roles(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL)
    role_ame = models.CharField('角色名', max_length=100)
    desc = models.CharField('描述', blank=True)
