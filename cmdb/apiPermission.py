from rest_framework import permissions
from .models.xroleModel import User


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
