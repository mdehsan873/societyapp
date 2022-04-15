from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import User,News,Visitor


admin.site.register(User)
admin.site.register(News)
admin.site.register(Visitor)