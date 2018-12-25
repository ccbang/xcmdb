from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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


class User(AbstractBaseUser):
    username = models.CharField('用户名称', max_length=200, unique=True)
    position = models.CharField('职位', blank=True, max_length=100)
    api_key = models.CharField('API接口密钥', blank=True, max_length=100)
    ssh_pub = models.TextField('SSH公钥', blank=True)
    avatar = models.ImageField(blank=True, null=True)
    group = models.ForeignKey(
        'Group',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
