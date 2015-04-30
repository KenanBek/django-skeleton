from django import forms
import django.contrib.auth.models as auth_models

from . import models

''' Login and Registration forms '''


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = auth_models.User
        fields = ('username', 'email', 'password')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = auth_models.User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('website', 'avatar')


''' User modify forms '''


class ModifyUserForm(forms.ModelForm):
    class Meta:
        model = auth_models.User
        fields = ('first_name', 'last_name', )


class ModifyProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('website', 'avatar', )