from rest_framework import serializers
from django.contrib.auth.models import Group
from user.models import User, Profile

class LoginInSerializer(serializers.Serializer):
    email = serializers.CharField()
    mobile = serializers.CharField()
    password = serializers.CharField()

class LoginOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"