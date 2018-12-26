from django.db import models
from django.utils import timezone
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, api_key, password=None):
        """
        创建普通用户，需要username和api_key
        """
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            api_key=api_key,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, api_key, password):
        """
        创建管理员
        """
        user = self.create_user(
            username,
            password=password,
            api_key=api_key,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


class User(AbstractBaseUser):
    username = models.CharField('用户名称', max_length=200, unique=True)
    name = models.CharField('用户名字', max_length=200)
    position = models.CharField('职位', blank=True, max_length=100)
    api_key = models.CharField('API接口密钥', blank=True, max_length=100)
    ssh_pub = models.TextField('SSH公钥', blank=True)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["api_key"]
    objects = MyUserManager()

    def get_all_permission(self):
        perm = set()

        # 从角色中获得操作权限
        if hasattr(self, 'members'):
            members = self.members.all()
            for member in members:
                perm.update(member.role.permission.values_list('codename', flat=True))

        return perm

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    class Meta:
        ordering = ("username", )
