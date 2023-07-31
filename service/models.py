from django.db import models
from common.models import *
from user.models import User

class VehicleType(Attributes):
    pass

class CargoType(Attributes):
    pass

class Driver(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_driver',
                             verbose_name="Ulanyjy")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE,
                                     related_name='vehicle_type_driver',
                                     verbose_name="Ulag görnüşi")
    
    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sürüji"
        verbose_name_plural = "Sürüjiler"

class Driver_Attribute(Attributes):
    class Meta:
        verbose_name = "Sürüji Atribýut"
        verbose_name_plural = "Sürüji Atribýutlar"

class Driver_Attribute_Value(Attribute_Values):
    attribute = models.ForeignKey(Driver_Attribute, on_delete=models.CASCADE,
                                  related_name='attribute_driver_attr_value',
                                  verbose_name="Attribýut")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,
                               related_name='driver_driver_attr_value',
                               verbose_name="Sürüji")
    
    class Meta:
        verbose_name = "Sürüji Atribýut Bahasy"
        verbose_name_plural = "Sürüji Atribýut Bahalary"
    
class DriverComment(CommentModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,
                               related_name='driver_driver_comment',
                               verbose_name="Sürüji")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_driver_comment',
                             verbose_name="Ulanyjy")

    def __str__(self):
        return str(self.driver.title_tm)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sürüji Teswir"
        verbose_name_plural = "Sürüji Teswirler"
    
class Cargo(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_cargo',
                             verbose_name="Ulanyjy")
    from_country = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name="Haýsy Ýurtdan")
    from_location = models.CharField(max_length=255, blank=True, null=True,
                                     verbose_name="Ýerleşýän ýerden")
    to_country = models.CharField(max_length=255, blank=True, null=True,
                                  verbose_name="Haýsy Ýurda")
    to_location = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name="Ýerleşýän ýere")
    weight = models.FloatField(blank=True, null=True,
                               verbose_name="Agramy")
    volume = models.FloatField(blank=True, null=True,
                               verbose_name="Göwrümi")
    price = models.FloatField(blank=True, null=True,
                              verbose_name="Bahasy")
    loading_date = models.DateField(blank=True, null=True,
                                    verbose_name="Ýüklenilýän wagty")
    unloading_date = models.DateField(blank=True, null=True,
                                      verbose_name="Düşürilýän wagty")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE,
                                     related_name='vehicle_type_cargo',
                                     verbose_name="Ulag görnüşi")
    cargo_type = models.ForeignKey(CargoType, on_delete=models.CASCADE,
                                   related_name='cargo_type_cargo',
                                   verbose_name="Ýük görnüşi")
    
    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kargo"
        verbose_name_plural = "Kargolar"

class CargoComment(CommentModel):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,
                              related_name='cargo_cargo_comment',
                              verbose_name="Ýük")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_cargo_comment',
                             verbose_name="Ulanyjy")
    
    def __str__(self):
        return str(self.cargo)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kargo Teswir"
        verbose_name_plural = "Kargo Teswirler"

class CargoAttribute(Attributes):
    pass

class CargoAttributeValue(Attribute_Values):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE,
                              related_name='cargo_cargo_attribute_value',
                              verbose_name="Ýük")
    attribute = models.ForeignKey(CargoAttribute, on_delete=models.CASCADE,
                                  related_name='attribute_cargo_attribute_value',
                                  verbose_name="Atribýut")
    
    class Meta:
        verbose_name = "Kargo Atr Bahasy"
        verbose_name_plural = "Kargo Atr Bahalary"

class WarehouseType(Attributes):
    class Meta:
        verbose_name = "Ammar görnüşi"
        verbose_name_plural = "Ammar görnüşler"

class Warehouse(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_warehouse',
                             verbose_name="Ulanyjy")
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE,
                                       related_name='warehouse_type_warehouse',
                                       verbose_name="Sklad görnüşi")
    capasity = models.FloatField(blank=True, null=True,
                                 verbose_name="Göwrümi")
    country = models.CharField(max_length=255, blank=True, null=True,
                               verbose_name="Ýurdy")
    location = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name="Ýerleşýän ýeri")
    is_available = models.BooleanField(default=True, verbose_name="Elýeterlimi")
    price = models.FloatField(blank=True, null=True, verbose_name="Bahasy")

    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ammar"
        verbose_name_plural = "Ammarlar"

class WarehouseAttribute(Attributes):
    class Meta:
        verbose_name = "Ammar Atribýut"
        verbose_name_plural = "Ammar Atribýutlar"

class WarehouseAttributeValue(Attribute_Values):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='warehouse_warehouse_attr_value',
                                  verbose_name="Ammar")
    attribute = models.ForeignKey(WarehouseAttribute, on_delete=models.CASCADE,
                                  related_name="attr_warehouse_attr_value",
                                  verbose_name="Atribýut")
    
    class Meta:
        verbose_name = "Ammar Attribýut Baha"
        verbose_name_plural = "Ammarlar Attribýut Bahalar"

class WarehouseComment(CommentModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='warehouse_warehouse_comment',
                                  verbose_name="Ammar")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_warehouse_comment',
                             verbose_name="Ulanyjy")
    
    def __str__(self):
        return str(self.warehouse)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ammar Teswir"
        verbose_name_plural = "Ammar Teswirler"

    
class Transport(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_transport',
                             verbose_name="Ulanyjy")
    is_local = models.BooleanField(default=False, verbose_name="Ýerlimi?")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE,
                                     related_name='vehicle_type_transport',
                                     verbose_name="Ulag görnüşi")
    from_country = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name="Haýsy ýurtdan")
    from_location = models.CharField(max_length=255, blank=True, null=True,
                                     verbose_name="Ýerleşýän ýerden")
    to_country = models.CharField(max_length=255, blank=True, null=True,
                                  verbose_name="Haýsy ýurda")
    to_location = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name="Ýerleşýän ýerden")
    due_date = models.DateField(blank=True, null=True, verbose_name="Sene")
    price = models.FloatField(blank=True, null=True, verbose_name="Bahasy")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ulag"
        verbose_name_plural = "Ulaglar"

class TransportAttribute(Attributes):
    class Meta:
        verbose_name = "Ulag Atribýut"
        verbose_name_plural = "Ulag Atribýutlar"

class TransportAttributeValue(Attribute_Values):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,
                                  related_name='transport_transport_attr_value',
                                  verbose_name="Ulag")
    attribute = models.ForeignKey(TransportAttribute, on_delete=models.CASCADE,
                                  related_name='attribute_transport_attr_value',
                                  verbose_name="Atribýut")
    
    class Meta:
        verbose_name = "Ulag atr Bahasy"
        verbose_name_plural = "Ulag atr Bahalar"

class TransportComment(CommentModel):
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,
                                  related_name='transport_transport_comment',
                                  verbose_name="Ammar")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_transport_comment',
                             verbose_name="Ulanyjy")
    
    def __str__(self):
        return str(self.transport)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Transport Teswir"
        verbose_name_plural = "Transport Teswirler"