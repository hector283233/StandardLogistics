from django.contrib import admin
from django.utils.html import format_html
from .models import *

class BannerAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;"/>'.format(obj.image_desktop.url))
    list_display = ['image_tag', 'title_tm', 'type', 'is_active']

class AdvertisementCommentInline(admin.StackedInline):
    model = AD_Comment
    extra = 1

class ADAttributeValuesInline(admin.StackedInline):
    model = AD_Attribute_Value
    extra = 1

class AdvertisementAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": (
            "user",
            "category",
            "is_active",
            "is_vip",
            "rating",
            "rating_count",
            "seen_count",
            "like_count"

        )}),
        (None, {"fields":(
            "title_tm",
            "title_ru",
            "title_en",
            "description_tm",
            "description_ru",
            "description_en",
            "price",
            "image1",
            "image2",
            "image3",
            "image4",
        )}
        )
    )
    def image_tag(self, obj):
        if obj.image1:
            return format_html('<img src="{0}" style="width: 45px; height:45px;"/>'.format(obj.image1.url))
        else:
            return "Surat Yok"
    inlines = [ADAttributeValuesInline, AdvertisementCommentInline]
    list_display = ("image_tag", "title_tm", "user", "is_active", "rating")
    list_display_links = ("image_tag", "title_tm", "user")
    list_filter = ("is_active", "is_vip", "category", "user", "created_at")
    search_fields = ("title_tm", "description_tm", "rating", "price")

admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerType)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(SubCategory)
admin.site.register(Category)
admin.site.register(AD_Attribute)
admin.site.register(AD_Attribute_Value)
admin.site.register(AD_Comment)