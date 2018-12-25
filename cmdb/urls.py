from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from cmdb.views.host import HostViewSet
from cmdb.views.member import MemberViewSet
from cmdb.views.project import ProjectViewSet
from cmdb.views.role import RoleViewSet
from cmdb.views.user import UserViewSet
from cmdb.apiPermission import CustomAuthToken


router.register(r'host', HostViewSet, base_name='host')
router.register(r'member', MemberViewSet, base_name='member')
router.register(r'project', ProjectViewSet, base_name='project')
router.register(r'role', RoleViewSet, base_name='role')
router.register(r'user', UserViewSet, base_name='user')

urlpatterns = [
    path("auth/", CustomAuthToken.as_view(), name="auth"),
] + router.urls