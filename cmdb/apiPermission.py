from rest_framework import permissions
from cmdb.models import User
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema


class CustomAuthToken(ObtainAuthToken):

    schema = ManualSchema(fields=[
        coreapi.Field(
            "username",
            required=True,
            location="form",
            description="用户名",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            description="用户密码",
            schema=coreschema.String()
        ),
    ], description="通过基本认证获取token")

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(type(user))
        token, created = Token.objects.get_or_create(user=user)
        role = ["user", "admin"] if user.is_staff else ["user"]

        return Response({
            'status': "ok",
            'type': "account",
            "currentAuthority": {
                'token': token.key,
                'id': user.pk,
                'email': user.email,
                'name': user.username,
                'role': role,
            }
        })



class BlacklistPermission(permissions.BasePermission):
    """
    检查用户是否有这个url的权限
    """

    def has_permission(self, request, view):
        user_pk = view.kwargs.get("user_pk", None)
        if user_pk is None:
            return False

        try:
            userObj = User.objects.get(pk=user_pk)
            this_perms = userObj.get_all_perssion()
            print(this_perms)
        except Exception as e:
            return False
        return False


class CustomObjectPermissions(permissions.DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }