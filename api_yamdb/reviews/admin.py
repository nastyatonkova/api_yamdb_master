from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import YaUser

class YaUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = YaUser
    list_display = ['email', 'username', 'first_name', 'last_name']

admin.site.register(YaUser, YaUserAdmin)