from django.db import models
from common.models import *
from user.models import User

class VehicleType(Attributes):
    pass

class Driver(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_driver')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE,
                                     related_name='vehicle_type_driver')
    
    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']

class Driver_Attribute(Attributes):
    pass

class Driver_Attribute_Value(Attribute_Values):
    attribute = models.ForeignKey(Driver_Attribute, on_delete=models.CASCADE,
                                  related_name='attribute_driver_attr_value')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,
                               related_name='driver_driver_attr_value')
    
class DriverComment(CommentModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE,
                               related_name='driver_driver_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_driver_comment')
    
    def __str__(self):
        return str(self.driver.title_tm)