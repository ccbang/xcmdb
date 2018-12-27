from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from cmdb.models import Credentials
from cmdb.serializers.credentials import CredentialsSerializer


class CredentialsViewSet(ModelViewSet):
    queryset = Credentials.objects.all()
    serializer_class =  CredentialsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('user'),