from rest_framework import serializers
from django.contrib.auth.models import Group
from user.models import (User, Profile, BusinessAccount,
                         BA_Attribute, BA_Attribute_Value)

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
    mobile_verified = serializers.BooleanField(required=False)
    email_verified = serializers.BooleanField(required=False)

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
                  "email_verified", "firebase_token", 'profile', 
                  'groups', "ads_count")
        
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "last_login", "username", "is_active", 
                  "date_joined", "mobile", "email", "mobile_verified",
                  "email_verified", "firebase_token", "ads_count")

class BAAttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BA_Attribute
        fields = "__all__"

class BAAttrValueListSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = BA_Attribute_Value
        fields = ["id", "title_tm", "title_ru", "title_en", "image",
                "value_tm", "value_ru", "value_en", "file",]
        
class BusinessAccountListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    attributes = BAAttrValueListSerializer(source="ba_value", many=True)
    class Meta:
        model = BusinessAccount
        fields = ["id", "is_verified", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "email", "facebook", "instagram", "telegram", "phone",
                  "image1", "image2", "image3", "image4", "file", "rating",
                  "rating_count", "created_at", "updated_at", "user", 
                  "attributes"]

class BusinessAccountDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    attributes = BAAttrValueListSerializer(source="ba_value", many=True)
    class Meta:
        model = BusinessAccount
        fields = ["id", "is_verified", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "email", "facebook", "instagram", "telegram", "phone",
                  "image1", "image2", "image3", "image4", "file", "rating",
                  "rating_count", "created_at", "updated_at", "user", 
                  "attributes"]

class BusinessAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAccount
        fields = ["id", "is_verified", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en", "email",
                  "facebook", "instagram", "telegram", "phone", "image1",
                  "image2", "image3", "image4", "file", "user"]
        
class BAAttributeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BA_Attribute
        fields = "__all__"

class BAAttributeValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BA_Attribute_Value
        fields = "__all__"

class BAAttributeValueOutSerializer(serializers.ModelSerializer):
    attribute = BAAttributeOutSerializer()
    class Meta:
        model = BA_Attribute_Value
        fields = ["id", "value_tm", "value_ru", "value_en", "file",
                  "attribute", "business_account"]

class BAAttributeValueDeleteSerializer(serializers.Serializer):
    business_account = serializers.IntegerField()

class BARatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()