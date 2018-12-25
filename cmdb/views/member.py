from rest_framework.viewsets import ModelViewSet
from cmdb.models import Member
from cmdb.serializers.member import MemberSerializer


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer