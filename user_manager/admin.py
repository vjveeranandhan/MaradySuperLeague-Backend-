from django.contrib import admin
from .models import CustomUser, UserType
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserType)