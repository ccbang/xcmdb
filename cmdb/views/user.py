from rest_framework.viewsets import ModelViewSet
from cmdb.models import User
from cmdb.serializers.user import UserSerializer


class UserViewSet(ModelViewSet):

    queryset =  User.objects.all()
    serializer_class = UserSerializer