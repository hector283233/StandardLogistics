from django.contrib import admin

from .models import *

class DriverAdminComment(admin.StackedInline):
    model = DriverComment
    extra = 1

class DriverAttributeValueAdmin(admin.StackedInline):
    model = Driver_Attribute_Value
    extra = 1

class DriverAdmin(admin.ModelAdmin):
    inlines = [DriverAdminComment, DriverAttributeValueAdmin]
    list_display = ('title_tm', "user", "is_active", "rating")
    list_filter = ("is_active", "rating", "is_vip", "created_at")
    search_fields = ("title_tm", "description_tm", "rating")
    

class CargoAdminComment(admin.StackedInline):
    model = CargoComment
    extra = 1

class CargoAttributeValueAdmin(admin.StackedInline):
    model = CargoAttributeValue
    extra = 1

class CargoAdmin(admin.ModelAdmin):
    inlines = [CargoAdminComment, CargoAttributeValueAdmin]
    list_display = ("title_tm", "user", "is_active", "rating")
    list_filter = ("is_active", "rating", "is_vip", "created_at")
    search_fields = ("title_tm", "description_tm", "rating", "price",
                     "loading_date", "from_country", "to_country",
                     "from_location", "to_location")
    
class WarehouseAttributeValueAdmin(admin.StackedInline):
    model = WarehouseAttributeValue
    extra = 1

class WarehouseAdmin(admin.ModelAdmin):
    inlines = [WarehouseAttributeValueAdmin]
    list_display = ("title_tm", "user", "is_active", "rating")
    list_filter = ("is_active", "rating", "is_vip", "created_at")
    search_fields = ["title_tm", "description_tm", "rating", 
                     "is_available", "capasity", "location"]

class TransportAttributeValueAdmin(admin.StackedInline):
    model = TransportAttributeValue
    extra = 1

class TransportAdmin(admin.ModelAdmin):
    inlines = [TransportAttributeValueAdmin]
    list_display = ("title_tm", "user", "is_active", "rating")
    list_filter = ("is_active", "rating", "is_vip", "created_at")
    search_fields = ["title_tm", "description_tm", "rating", "price",
                     "from_location", "from_country", "to_country",
                     "to_location", "due_date"]


admin.site.register(VehicleType)
admin.site.register(CargoType)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Driver_Attribute)
admin.site.register(Driver_Attribute_Value)
admin.site.register(DriverComment)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(CargoComment)
admin.site.register(CargoAttribute)
admin.site.register(CargoAttributeValue)
admin.site.register(WarehouseType)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(WarehouseAttribute)
admin.site.register(WarehouseAttributeValue)
admin.site.register(WarehouseComment)
admin.site.register(Transport, TransportAdmin)
admin.site.register(TransportAttribute)
admin.site.register(TransportAttributeValue)
admin.site.register(TransportComment)