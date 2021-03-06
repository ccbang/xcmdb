from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from avatar_generator import Avatar


from .hosts import Host
from .job import Job, JobHost
from .user import  User
from .role import Role, RoleGroup
from .template import Tasks, RoleTemplate
from .project import Project, Member
from .credentials import Credentials



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # 当收到users表创建用户时将触发创建用户对应的token，用于验证登陆
    if created:
        Token.objects.create(user=instance)
        if not instance.avatar:  # 如果用户没有头像，则自动创建一个
            avatar_name = "{}/avatar/{}.png".format(
                settings.MEDIA_ROOT, instance.username)
            with open(avatar_name, 'wb') as atf:
                atf.write(Avatar.generate(128, instance.username))
            instance.avatar = avatar_name
            instance.save()
