from django import forms
import django.contrib.auth.models as auth_models
import hashlib
import datetime
import random
from django.core.mail import send_mail

from . import models

''' Login and Registration forms '''


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    repeat_new_password = forms.CharField(widget=forms.PasswordInput())


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())
    repeat_new_password = forms.CharField(widget=forms.PasswordInput())


class RestorePasswordForm(forms.Form):
    email = forms.EmailField()


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
        fields = ('username', 'email', 'first_name', 'last_name', )

    def save(self, commit=True):
        instance = super(ModifyUserForm, self).save(commit=False)
        user = auth_models.User.objects.get(id=instance.id)
        instance.email = user.email
        if self.cleaned_data['email'] != user.email:
            instance.profile.is_verified = False
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            request, created = models.EmailChangeRequest.objects.get_or_create(user=user)
            request.new_email = self.cleaned_data['email']
            request.activation_key = hashlib.sha1(salt+request.new_email).hexdigest()
            request.key_expires = datetime.datetime.today() + datetime.timedelta(2)
            request.save()
            # Send email with activation key
            email_subject = 'Email change confirmation'
            email_body = "Hey %s. To activate your new email, click this link within 48hours" \
                         "\nhttp://localhost:8000/account/change/%s" % (user.username, request.activation_key)

            send_mail(email_subject, email_body, "noreply@tapdoon.email", [request.new_email], fail_silently=False)
        if commit:
            instance.save()
        return instance


class ModifyProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('website', 'avatar', )