from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from user.models import *

class CustomUserChange(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": (
            "username", 
            "password",
            "email",
            "email_verified",
            "mobile",
            "mobile_verified",
            "firebase_token",
            "ads_count",
            )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    
    list_display = ("username", "is_staff", "email")
    list_filter = ("is_active", "groups", "mobile_verified", "email_verified")
    search_fields = ("first_name", "last_name", "country", "city")
    ordering = ("-date_joined",)
    form = CustomUserChange

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "country", "city")
    list_filter = ("user", "first_name", "last_name", "country", "city")
    search_fields = ("first_name", "last_name", "country", "city")

class BusinessAttributeInline(admin.StackedInline):
    model = BA_Attribute_Value
    extra = 3

class BusinessAccountAdmin(admin.ModelAdmin):
    model = BusinessAccount
    inlines = [BusinessAttributeInline]
    list_display = ("title_tm", "is_active", "is_verified", 'rating')
    list_filter = ('is_active', "is_verified", 'rating')
    search_fields = ("email", "facebook", "instagram", "telegram", "phone")

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserId)
admin.site.register(BusinessAccount, BusinessAccountAdmin)
admin.site.register(BA_Attribute)