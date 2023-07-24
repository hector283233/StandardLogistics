from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserId(models.Model):
    user_id = models.IntegerField()

class User(AbstractUser):
    mobile = models.CharField(max_length=255, null=True, blank=True,
                              verbose_name="Mobile")
    mobile_verified = models.BooleanField(default=False,
                                          verbose_name="Mobil tassyklananmy")
    email_verified = models.BooleanField(default=False,
                                         verbose_name="Email tassyklananmy")
    firebase_token = models.CharField(max_length=255, null=True, blank=True)
    ads_count = models.IntegerField(default=0, verbose_name="Bildiriş sany")

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
        verbose_name = "Ulanyjy"
        verbose_name_plural = "Ulanyjylar"


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE,
                                related_name="profile_user",
                                verbose_name="Ulanyjy")
    first_name = models.CharField(max_length=64, blank=True, null=True,
                                  verbose_name="Ady")
    last_name = models.CharField(max_length=64, blank=True, null=True,
                                 verbose_name="Familiýasy")
    country = models.CharField(max_length=64, blank=True, null=True,
                               verbose_name="Ýurdy")
    city = models.CharField(max_length=64, blank=True, null=True,
                            verbose_name="Şäher")
    address = models.CharField(max_length=255, blank=True, null=True,
                               verbose_name="Adres")
    description = models.TextField(blank=True, null=True,
                                   verbose_name="Giňişleýin")
    ad_count = models.IntegerField(default=0, verbose_name="Bildiriş sany")
    file = models.FileField(upload_to="profile/", blank=True, null=True,
                            verbose_name="Faýl")
    image = models.ImageField(upload_to="profile/", blank=True, null=True,
                              verbose_name="Surat")

    def __str__(self):
        return str(self.user.username)
    
    
class BusinessAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='business_account_user',
                                verbose_name="Ulanyjy")
    is_active = models.BooleanField(default=True,
                                    verbose_name="Aktiwmy?")
    is_verified = models.BooleanField(default=False,
                                      verbose_name="Tassyklanamy?")
    title_tm = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Ady (tm)")
    title_ru = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Ady (ru)")
    title_en = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name="Ady (en)")
    description_tm = models.TextField(blank=True, null=True,
                                      verbose_name="Giňişleýin (tm)")
    description_ru = models.TextField(blank=True, null=True,
                                      verbose_name="Giňişleýin (ru)")
    description_en = models.TextField(blank=True, null=True,
                                      verbose_name="Giňişleýin (en)")
    email = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image1 = models.ImageField(upload_to='business_img/', blank=True, null=True,
                               verbose_name="Surat 1")
    image2 = models.ImageField(upload_to='business_img/', blank=True, null=True,
                               verbose_name="Surat 2")
    image3 = models.ImageField(upload_to='business_img/', blank=True, null=True, 
                               verbose_name="Surat 3")
    image4 = models.ImageField(upload_to='business_img/', blank=True, null=True, 
                               verbose_name="Surat 4")
    file = models.FileField(upload_to='business_file/', blank=True, null=True, 
                            verbose_name="Faýl")
    rating = models.FloatField(default=0, verbose_name="Reýting")
    rating_count = models.IntegerField(default=0, verbose_name="Reýting Sany")
    seen_count = models.IntegerField(default=0, verbose_name="Görülen Sany")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Biznes Akkaunt"
        verbose_name_plural = "Biznes Akkauntrlar"
    
class BA_Attribute(models.Model):
    title_tm = models.CharField(max_length=255, verbose_name="Ady (tm)")
    title_ru = models.CharField(max_length=255, verbose_name="Ady (ru)", blank=True, null=True)
    title_en = models.CharField(max_length=255, verbose_name="Ady (en)", blank=True, null=True)
    image = models.ImageField(upload_to='attributes/', blank=True, null=True,
                              verbose_name="Surat")

    def __str__(self):
        return str(self.title_tm)
    
    class Meta:
        verbose_name = "Biznes Akkaunt Atribýut"
        verbose_name_plural = "Biznes Akkaunt Atribýutlar"

class BA_Attribute_Value(models.Model):
    attribute = models.ForeignKey(BA_Attribute, on_delete=models.CASCADE,
                                  related_name='ba_attr_value',
                                  verbose_name="Atribýut")
    business_account = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE,
                                         related_name='ba_value',
                                         verbose_name="Biznes Akkaunt")
    value_tm = models.CharField(max_length=255, verbose_name="Baha (tm)", blank=True, null=True)
    value_ru = models.CharField(max_length=255, verbose_name="Baha (ru)", blank=True, null=True)
    value_en = models.CharField(max_length=255, verbose_name="Baha (en)", blank=True, null=True)
    file = models.FileField(upload_to='attributes/', blank=True, null=True,
                            verbose_name="Faýl")

    def __str__(self):
        return str(self.value_tm)
    
    class Meta:
        verbose_name = "Biznes Akkaunt Atribýut Bahasy"
        verbose_name_plural = "Biznes Akkaunt Atribýut Bahalary"