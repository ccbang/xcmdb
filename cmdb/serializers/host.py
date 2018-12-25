from rest_framework import serializers
from cmdb.models import Host


class HostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Host
        fields = "__all__"