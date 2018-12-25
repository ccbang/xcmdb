from rest_framework import serializers
from cmdb.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password",)