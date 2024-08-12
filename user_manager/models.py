from django.contrib.auth.models import AbstractUser
from django.db import models

class UserType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='profile_images/')
    age = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=False, null=False, verbose_name='Phone Number')
    user_type = models.ManyToManyField(UserType, blank=True)

    def __str__(self):
        return self.username