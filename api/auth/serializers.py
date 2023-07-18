from rest_framework import serializers
from django.contrib.auth.models import Group
from user.models import User, Profile

class LoginInSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )

class LoginOutSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')

class RegisterInSerializer(LoginInSerializer):
    pass

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserUpdateSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)

class ProfileOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'country', 'city',
                  'address', 'description', 'ad_count', 
                  'file', 'image']

class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    profile = ProfileOutSerializer(source="profile_user")
    class Meta:
        model = User
        fields = ("id", "last_login", "username", "is_active", 
                  "date_joined", "mobile", "email", "mobile_verified",
                  "email_verified", "firebase_token", 'profile', 'groups')
        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "last_login", "username", "is_active", 
                  "date_joined", "mobile", "email", "mobile_verified",
                  "email_verified", "firebase_token")