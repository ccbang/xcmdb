from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from avatar_generator import Avatar


from .hosts import Host
from .job import Job, JobHost
from .permission import AuthGroup, AuthPermission
from .user import  User
from .role import Group, Role
from .template import Tasks, RoleTemplate
from .project import Project, Member



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if not instance.avatar:
            avatar_name = "{}/avatar/{}.png".format(
                settings.MEDIA_ROOT, instance.username)
            with open(avatar_name, 'wb') as atf:
                atf.write(Avatar.generate(128, instance.username))
            instance.avatar = avatar_name
            instance.save()
