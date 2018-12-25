### 需要安装的工具

- django >=2.0
- ansible
- djangorestframework
- django_filters
- avatar_generator

```config
现在处于开发阶段，大部分功能会随时改变，仅供大家讨论学习。 
```

#### 用户认证/权限
```config
# 每个view可以按照自定义去覆盖以下默认方法
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 默认所有api必须认证
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (  # 默认认证方式
        'rest_framework.authentication.BasicAuthentication', 
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (  # 默认使用django_filters进行筛选
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}
```