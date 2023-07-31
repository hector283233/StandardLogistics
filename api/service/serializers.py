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
    class Meta:
        model = Driver
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "user"]
    
    def get_comments(self, obj):
        qs = DriverComment.objects.filter(is_active=True, driver=obj)
        serializer = DriverCommentOutSerializer(instance=qs, many=True)
        return serializer.data

class DriversDetailSerializer(serializers.ModelSerializer):
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
        exclude = ('is_active', 'rating', 'rating_count', 'like_count', 
                   'seen_count', 'is_vip')

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
        exclude = ('is_active', )

class CommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "mobile", "email"]

class DriverCommentCreateOutSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    class Meta:
        model = DriverComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "driver", "user"]
        
class CargoListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Cargo
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "from_country", "from_location", "to_country",
                  "to_location", "weight", "volume", "price", "loading_date",
                  "unloading_date", "vehicle_type", "cargo_type", "user"]

class CargoCommentOutSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    class Meta:
        model = CargoComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "cargo", "user"]

class CargoAttrValueCreateOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = CargoAttributeValue
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]
        
class CargoCargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = "__all__"

class CargoDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = UserDetailSerializer()
    attributes = CargoAttrValueCreateOutSerializer(
        source="cargo_cargo_attribute_value", many=True)
    vehicle_type = DriverVehicleTypeOutSerializer()
    cargo_type = CargoCargoTypeSerializer()
    class Meta:
        model = Cargo
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "from_country", "from_location", "to_country",
                  "to_location", "weight", "volume", "price", "loading_date",
                  "unloading_date", "vehicle_type", "cargo_type", "user",
                  "comments", "attributes"]
    
    def get_comments(self, obj):
        qs = CargoComment.objects.filter(is_active=True, cargo=obj)
        serializer = CargoCommentOutSerializer(instance=qs, many=True)
        return serializer.data

class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        exclude = ('is_active', 'rating', 'rating_count', 'like_count', 
                   'seen_count', 'is_vip')

class CargoAttrValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoAttributeValue
        fields = "__all__"

class CargoCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoComment
        exclude = ("is_active", )

class CargoCommentCreateOutSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    class Meta:
        model = CargoComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "cargo", "user"]
        
class WarehouseWarehouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseType
        fields = "__all__"

class WarehouseCommentCreateOutSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    class Meta:
        model = WarehouseComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "warehouse", "user"]

class WarehouseAttrValueCreateOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = WarehouseAttributeValue
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]

class WarehouseListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Warehouse
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "country", "location", "capasity", "price", "is_available",
                  "user"]
        
class WarehouseDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    warehouse_type = WarehouseWarehouseTypeSerializer()
    comments = serializers.SerializerMethodField()
    attributes = WarehouseAttrValueCreateOutSerializer(
        source="warehouse_warehouse_attr_value", many=True)
    class Meta:
        model = Warehouse
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "country", "location", "capasity", "price", "is_available",
                  "warehouse_type", "comments", "attributes", "user"]
    
    def get_comments(self, obj):
        qs = WarehouseComment.objects.filter(is_active=True, warehouse=obj)
        serializer = WarehouseCommentCreateOutSerializer(instance=qs, many=True)
        return serializer.data



class WarehouseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        exclude = ('is_active', 'rating', 'rating_count', 'like_count', 
                   'seen_count', 'is_vip')

class WarehouseAttrValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseAttributeValue
        fields = "__all__"

class WarehouseCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseComment
        exclude = ('is_active',)



class TransportCommentCreateOutSerializer(serializers.ModelSerializer):
    user = CommentUserSerializer()
    class Meta:
        model = TransportComment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "transport", "user"]
            
class TransportAttrValueCreateOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = TransportAttributeValue
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]


class TransportListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Transport
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "from_country", "from_location", "is_local", "price", 
                  "due_date", "user"]

class TransportDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    vehicle_type = DriverVehicleTypeOutSerializer()
    comments = serializers.SerializerMethodField()
    attributes = TransportAttrValueCreateOutSerializer(
        source="transport_transport_attr_value", many=True)
    class Meta:
        model = Transport
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating",
                  "rating_count", "seen_count", "like_count", "created_at",
                  "from_country", "from_location", "is_local", "price", 
                  "due_date", "user", "vehicle_type", "attributes", "comments"]
    
    def get_comments(self, obj):
        qs = TransportComment.objects.filter(is_active=True, transport=obj)
        serializer = TransportCommentCreateOutSerializer(instance=qs, many=True)
        return serializer.data

class TransportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        exclude = ('is_active', 'rating', 'rating_count', 'like_count', 
                   'seen_count', 'is_vip')

class TransportAttrValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportAttributeValue
        fields = "__all__"

class TransportCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportComment
        exclude = ('is_active',)

