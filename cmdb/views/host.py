from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from cmdb.models import Host
from cmdb.serializers.host import HostSerializer


class HostViewSet(ModelViewSet):
    '''
    list: 机器列表
    '''
    queryset = Host.objects.all()
    serializer_class =  HostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('hostname', 'project')