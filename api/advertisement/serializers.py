from rest_framework import serializers
from advertisement.models import *
from user.models import *
from GlobalVariables import *

from api.auth.serializers import UserDetailSerializer

class ADAttributesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Attribute
        fields = "__all__"

class BannerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerType
        fields = "__all__"

class CategoryBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SubcategoryBannerSerializer(serializers.ModelSerializer):
    main_category = CategoryBannerSerializer()
    class Meta:
        model = SubCategory
        fields = ["id", "title_tm", "title_ru", "title_en",
                  "image", "main_category"]

class BannerListSerializer(serializers.ModelSerializer):
    type = BannerTypeSerializer()
    category = SubcategoryBannerSerializer()
    class Meta:
        model = Banner
        fields = ["id", "title_tm", "title_ru", "title_en",
                  "subtitle_tm", "subtitle_ru", "subtitle_en",
                  "image_desktop", "image_mobile", "created_at",
                  "type", "category"]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "title_tm", "title_ru", "title_en", "image"]

class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(source="upper_category", many=True)
    class Meta:
        model = Category
        fields = ["id", "title_tm", "title_ru", "title_en",
                  "image", "subcategories"]

class UserADCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "mobile", "first_name", "last_name"]

class ADCommentOutSerializer(serializers.ModelSerializer):
    user = UserADCommentSerializer()
    class Meta:
        model = AD_Comment
        fields = ["id", "title", "description", "is_notified", 
                  "created_at", "user"]

class ADAttributeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Attribute
        fields = "__all__"

class ADAttributeValueOutSerializer(serializers.ModelSerializer):
    title_tm = serializers.CharField(source="attribute.title_tm")
    title_ru = serializers.CharField(source="attribute.title_ru")
    title_en = serializers.CharField(source="attribute.title_en")
    image = serializers.ImageField(source="attribute.image")
    class Meta:
        model = AD_Attribute_Value
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "title_tm", "title_ru", "title_en",
                  "image"]

class AdvertisementListSerializer(serializers.ModelSerializer):
    category = SubCategorySerializer()
    user = UserDetailSerializer()
    comments = serializers.SerializerMethodField()
    attributes = ADAttributeValueOutSerializer(source="atvertisement_attr_value", many=True)
    class Meta:
        model = Advertisement
        fields = ["id", "is_vip", "title_tm", "title_ru", "title_en", 
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "rating", 
                  "rating_count", "seen_count", "like_count", "created_at",
                  "price", "user", "category", "comments", "attributes"]
    
    def get_comments(self, obj):
        qs = AD_Comment.objects.filter(is_active=True, advertisement=obj)
        serializer = ADCommentOutSerializer(instance=qs, many=True)
        return serializer.data

class AdvertisementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ["id", "title_tm", "title_ru", "title_en",
                  "description_tm", "description_ru", "description_en",
                  "image1", "image2", "image3", "image4", "price",
                  "category", "user"]
        

class ADAttributeValueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Attribute_Value
        fields = "__all__"

class ADAttributeOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Attribute
        fields = "__all__"

class ADAttributeUOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Attribute
        fields = "__all__"

class ADAttributeValueUOutSerializer(serializers.ModelSerializer):
    attribute = ADAttributeUOutSerializer()
    class Meta:
        model = AD_Attribute_Value
        fields = ["id", "value_tm", "value_ru", "value_en",
                  "file", "attribute"]
        
class ADCommentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name",
                  "mobile", "email"]
class ADCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AD_Comment
        exclude = ("is_active", )

class ADCommentCreateOutSerializer(serializers.ModelSerializer):
    user = ADCommentUserSerializer()
    class Meta:
        model = AD_Comment
        fields = ["id", "title", "description", "is_notified",
                  "created_at", "advertisement", "user"]