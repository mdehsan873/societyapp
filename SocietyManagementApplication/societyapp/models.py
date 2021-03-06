from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager

class OTPLog(models.Model):
    email = models.EmailField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.otp)


class User(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    mobile_no=models.IntegerField(default=0)
    flat_no=models.IntegerField(default=0)
    tower_no=models.IntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now())
    is_superuser=models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email