from rest_framework import serializers
from service.models import *
from user.models import *
from GlobalVariables import *

from api.auth.serializers import UserDetailSerializer

class VehicleTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"

class CargoTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = "__all__"

class WarehouseTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseType
        fields = "__all__"

class DriverAttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Attribute
        fields = "__all__"

class CargoAttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoAttribute
        fields = "__all__"

class WarehouseAttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAttribute
        fields = "__all__"

class TransportAttrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportAttribute
        fields = "__all__"

class DriverAttributeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Attribute
        fields = "__all__"

class DriverCommentOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverComment
        fields = "__all__"

class DriverAttrOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Attribute
        fields = "__all__"

class DriverAttrValueOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = Driver_Attribute_Value
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]

class DriverVehicleTypeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"

class DriversListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    comments = serializers.SerializerMethodField()
    attributes = DriverAttrValueOutSerializer(source="driver_driver_attr_value", many=True)
    vehicle_type = DriverVehicleTypeOutSerializer()
    class Meta:
        model = Driver
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "user", "comments", "attributes", "vehicle_type"]
    
    def get_comments(self, obj):
        qs = DriverComment.objects.filter(is_active=True, driver=obj)
        serializer = DriverCommentOutSerializer(instance=qs, many=True)
        return serializer.data

class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class DriverAttrValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver_Attribute_Value
        fields = "__all__"

class DriverAttrValueCreateOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = Driver_Attribute_Value
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]
        
class DriverCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverComment
        fields = "__all__"

class DriverCommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "mobile", "email"]

class DriverCommentCreateOutSerializer(serializers.ModelSerializer):
    user = DriverCommentUserSerializer()
    class Meta:
        model = DriverComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "driver", "user"]
        
class CargoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"