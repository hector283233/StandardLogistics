from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserId(models.Model):
    user_id = models.IntegerField()

class User(AbstractUser):
    mobile = models.CharField(max_length=255, null=True, blank=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    firebase_token = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.is_superuser or not self.is_staff:
                last_user = UserId.objects.latest('id')
                uid = int(last_user.user_id) + 1
                self.username = str(uid)
                last_user.user_id = uid
                last_user.save()
            super(User, self).save(*args, **kwargs)
            Profile.objects.create(user=self)
        else:
            super(User, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-date_joined', )


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE,
                                related_name="profile_user")
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ad_count = models.IntegerField(default=0)
    file = models.FileField(upload_to="profile/", blank=True, null=True)
    image = models.ImageField(upload_to="profile/", blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
    
class BusinessAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='business_account_user')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    title_tm = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    title_en = models.CharField(max_length=255, null=True, blank=True)
    description_tm = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image1 = models.ImageField(upload_to='business_img/', blank=True, null=True)
    image2 = models.ImageField(upload_to='business_img/', blank=True, null=True)
    image3 = models.ImageField(upload_to='business_img/', blank=True, null=True)
    image4 = models.ImageField(upload_to='business_img/', blank=True, null=True)
    file = models.FileField(upload_to='business_file/', blank=True, null=True)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
class BA_Attribute(models.Model):
    title_tm = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    image = models.ImageField(upload_to='attributes/', blank=True, null=True)

    def __str__(self):
        return str(self.title_tm)

class BA_Attribute_Value(models.Model):
    attribute = models.ForeignKey(BA_Attribute, on_delete=models.CASCADE,
                                  related_name='ba_attr_value')
    business_account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE,
                                         related_name='ba_value')
    value_tm = models.CharField(max_length=255)
    value_ru = models.CharField(max_length=255)
    value_en = models.CharField(max_length=255)
    file = models.FileField(upload_to='attributes/', blank=True, null=True)

    def __str__(self):
        return str(self.value_tm)