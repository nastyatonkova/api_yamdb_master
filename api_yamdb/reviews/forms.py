from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import YaUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = YaUser
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = YaUser
        fields = ('username', 'email', 'first_name', 'last_name')