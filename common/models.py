from django.db import models

class Attributes(models.Model):
    title_tm = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to='attributes/', blank=True, null=True)

    def __str__(self):
        return str(self.title_tm)
    
class Attribute_Values(models.Model):
    value_tm = models.CharField(max_length=255)
    value_ru = models.CharField(max_length=255)
    value_en = models.CharField(max_length=255)
    file = models.FileField(upload_to='attributes/', blank=True, null=True)

    def __str__(self):
        return str(self.value_tm)
    
class CommonModel(models.Model):
    is_active = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    title_tm = models.CharField(max_length=255, blank=True, null=True)
    title_ru = models.CharField(max_length=255, blank=True, null=True)
    title_en = models.CharField(max_length=255, blank=True, null=True)
    description_tm = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)
    image3 = models.ImageField(upload_to='services/', blank=True, null=True)
    image4 = models.ImageField(upload_to='services/', blank=True, null=True)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    seen_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']