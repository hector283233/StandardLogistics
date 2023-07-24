from django.db import models
from common.models import *
from user.models import User

class Category(Attributes):
    class Meta:
        verbose_name = "Kategoriýa"
        verbose_name_plural = "Kategoriýalar"

class SubCategory(Attributes):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='upper_category',
                                 verbose_name="Esasy kategoriýa")
    
    class Meta:
        verbose_name = "Içki kategoriýa"
        verbose_name_plural = "Içki kategoriýalar"

class BannerType(models.Model):
    title = models.CharField(max_length=255, verbose_name="Ady")

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Banner Görnüşi"
        verbose_name_plural = "Banner Görnüşleri"

class Banner(models.Model):
    title_tm = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (tm)")
    title_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (ru)")
    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (en)")
    subtitle_tm = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle (tm)")
    subtitle_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle (ru)")
    subtitle_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle (en)")
    image_desktop = models.ImageField(upload_to='banners/', verbose_name="Surat Uly")
    image_mobile = models.ImageField(upload_to='banners/', verbose_name="Surat kiçi")
    is_active = models.BooleanField(default=True, verbose_name="Aktiwmy?")
    type = models.ForeignKey(BannerType, on_delete=models.CASCADE,
                             related_name='type_banner', verbose_name="Banner görnüşi")
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name="Kategoriýa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"

class Advertisement(CommonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_advertisement',
                             verbose_name="Ulanyjy")
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, 
                                 related_name='category_ads',
                                 verbose_name="Kategoriýa")
    price = models.FloatField(default=0, verbose_name="Bahasy")


    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bildiriş"
        verbose_name_plural = "Bildirişler"

class AD_Attribute(Attributes):
    class Meta:
        verbose_name = "Bildiriş atribýut"
        verbose_name_plural = "Bildiriş atribýutlar"

class AD_Attribute_Value(Attribute_Values):
    attribute = models.ForeignKey(AD_Attribute, on_delete=models.CASCADE,
                                  related_name='advertisement_attr',
                                  verbose_name="Attribýut")
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      related_name='atvertisement_attr_value',
                                      verbose_name="Bildiriş")
    
    class Meta:
        verbose_name = "Bildiriş Atr Bahasy"
        verbose_name_plural = "Bildiriş Attr Bahalary"
    
class AD_Comment(CommentModel):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE,
                                      related_name='advertisement_comment', 
                                      verbose_name="Bildiriş")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_comment',
                             verbose_name="Ulanyjy")
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Advertisement Comment"
        verbose_name_plural = "Advertisement Comments"
