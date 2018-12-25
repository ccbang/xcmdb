from rest_framework.viewsets import ModelViewSet
from cmdb.models import Role
from cmdb.serializers.role import RoleSerializer


class RoleViewSet(ModelViewSet):

    queryset = Role.objects.all()
    serializer_class = RoleSerializer