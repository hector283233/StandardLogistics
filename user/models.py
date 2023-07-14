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
    
    class Meta:
        ordering = ('-date_joined', )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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