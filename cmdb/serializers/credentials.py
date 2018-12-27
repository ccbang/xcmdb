from rest_framework import serializers
from cmdb.models import Credentials


class CredentialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Credentials
        fileds = "__all__"


