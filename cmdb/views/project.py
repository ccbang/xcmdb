from rest_framework.viewsets import ModelViewSet
from cmdb.models import Project
from cmdb.serializers.project import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
