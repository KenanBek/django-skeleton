from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import django.contrib.auth as django_auth

from core.utils.decorators import anonymous_required
from account import models
from account import forms


def index(request, template="user/account/index.html", context={}):
    return render(request, template, context)


@anonymous_required
def login(request, template="user/account/login.html", context={}):
    next_url = request.GET.get('next', False)
    login_form = forms.LoginForm(request.POST or None)

    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = django_auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, _('You have successfully logged in.'))
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect(reverse('index'))
                else:
                    messages.add_message(request, messages.WARNING, _('Non active user.'))
            else:
                messages.add_message(request, messages.ERROR, _('Wrong username or password.'))

    context['login_form'] = login_form
    return render(request, template, context)


@anonymous_required
def register(request, template="user/account/register.html", context={}):
    user_form = forms.UserForm(request.POST or None)
    profile_form = forms.ProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_username = user_form.cleaned_data['username']
            user_email = user_form.cleaned_data['email']
            user_password = user_form.cleaned_data['password']

            user = user_form.save(commit=False)
            if user.email and User.objects.filter(email=user_email).exclude(username=user_username).count():
                errors = user_form._errors.setdefault("email", ErrorList())
                errors.append(_('User with this Email already exists.'))
                messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
            else:
                user.set_password(user_password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.add_message(request, messages.SUCCESS, _('You have successfully registered.'))
                user = django_auth.authenticate(username=user_username, password=user_password)
                django_auth.login(request, user)
                return redirect(reverse('account_index'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)


@login_required
def logout(request):
    django_auth.logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have successfully logged out.'))
    return redirect(reverse('index'))


def modify_account(request, template="user/account/account_modify.html", context={}):
    user_form = None
    profile_form = None

    if not hasattr(request.user, 'profile'):
        request.user.profile = models.Profile()

    if request.method == 'POST':
        user_form = forms.ModifyUserForm(request.POST or None, instance=request.user)
        profile_form = forms.ModifyProfileForm(request.POST or None, request.FILES or None,
            instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, _('Your account successfully modified.'))
            return redirect(reverse('account_index'))
        else:
            messages.add_message(request, messages.ERROR, _('Some errors occurred. Please fix errors bellow.'))
    else:
        user = request.user
        user_form = forms.ModifyUserForm(instance=user)
        profile_form = forms.ModifyProfileForm(instance=user.profile)

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)

