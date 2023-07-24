from django.db import models

class Attributes(models.Model):
    title_tm = models.CharField(max_length=255, verbose_name="Ady (tm)")
    title_ru = models.CharField(max_length=255, verbose_name="Ady (ru)")
    title_en = models.CharField(max_length=255, verbose_name="Ady (en)")
    image = models.ImageField(upload_to='attributes/', blank=True, null=True, verbose_name="Surat")

    def __str__(self):
        return str(self.title_tm)
    
class Attribute_Values(models.Model):
    value_tm = models.CharField(max_length=255, verbose_name="Bahasy (tm)",
                                blank=True, null=True)
    value_ru = models.CharField(max_length=255, verbose_name="Bahasy (ru)",
                                blank=True, null=True)
    value_en = models.CharField(max_length=255, verbose_name="Bahasy (en)",
                                blank=True, null=True)
    file = models.FileField(upload_to='attributes/', blank=True, null=True, verbose_name="Faýl")

    def __str__(self):
        return str(self.value_tm)
    
class CommonModel(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Aktiwmy?")
    is_vip = models.BooleanField(default=False, verbose_name="Wipmy?")
    title_tm = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (tm)")
    title_ru = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (ru)")
    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady (en)")
    description_tm = models.TextField(blank=True, null=True, verbose_name="Giňişleýin (tm)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Giňişleýin (ru)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Giňişleýin (en)")
    image1 = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Surat 1")
    image2 = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Surat 2")
    image3 = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Surat 3")
    image4 = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Surat 4")
    rating = models.FloatField(default=0, verbose_name="Reýting")
    rating_count = models.IntegerField(default=0, verbose_name="Reýting sany")
    seen_count = models.IntegerField(default=0, verbose_name="Görülen sany")
    like_count = models.IntegerField(default=0, verbose_name="Halanan sany")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Aktiwmy?")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ady")
    description = models.TextField(blank=True, null=True, verbose_name="Giňişleýin")
    is_notified = models.BooleanField(default=False, verbose_name="Notifikasiýa ugradylanmy?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']