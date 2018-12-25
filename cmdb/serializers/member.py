from rest_framework import serializers
from cmdb.models import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = "__all__"