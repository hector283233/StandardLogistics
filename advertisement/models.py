from django.db import models
from common.models import *
from user.models import User

class BannerType(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)

class Banner(models.Model):
    title_tm = models.CharField(max_length=255, blank=True, null=True)
    title_ru = models.CharField(max_length=255, blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    subtitle_tm = models.CharField(max_length=255, blank=True, null=True)
    subtitle_ru = models.CharField(max_length=255, blank=True, null=True)
    subtitle_en = models.CharField(max_length=255, blank=True, null=True)
    image_desktop = models.ImageField(upload_to='banners/')
    image_mobile = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    type = models.ForeignKey(BannerType, on_delete=models.CASCADE,
                             related_name='type_banner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']


class Category(Attributes):
    pass

class SubCategory(Attributes):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='upper_category')

class Advertisement(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_advertisement')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, 
                                 related_name='category_ads')
    price = models.FloatField(default=0)


    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']

class AD_Attribute(Attributes):
    pass

class AD_Attribute_Value(Attribute_Values):
    attribute = models.ForeignKey(AD_Attribute, on_delete=models.CASCADE,
                                  related_name='advertisement_attr')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      related_name='atvertisement_attr_value')
    
class AD_Comment(CommentModel):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      related_name='advertisement_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_comment')
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Advertisement Comment"
        verbose_name_plural = "Advertisement Comments"
