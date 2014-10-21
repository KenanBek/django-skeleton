from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from core.decorators import anonymous_required
import forms


def index(request, template="bootstrap3/account/index.html", context={}):
    return render(request, template, context)


@anonymous_required
def login(request, template="bootstrap3/account/login.html", context={}):
    next_url = request.GET.get('next', False)
    login_form = forms.LoginForm(request.POST or None)

    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    messages.add_message(request, messages.SUCCESS, _('You have successfully logged in.'))
                    if next:
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
def register(request, template="bootstrap3/account/register.html", context={}):
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
                user = authenticate(username=user_username, password=user_password)
                auth_login(request, user)
                return redirect(reverse('account_index'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)


@login_required
def logout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have successfully logged out.'))
    return redirect(reverse('index'))


def login_facebook(request, template="bootstrap3/account/login_facebook.html", context={}):
    return render(request, template, context)


@anonymous_required
def auth(request, template="bootstrap3/account/auth.html", context={}):
    login_form = forms.LoginForm(request.POST or None)
    register_form = forms.RegisterForm(request.POST or None)

    context['login_form'] = login_form
    context['register_form'] = register_form
    return render(request, template, context)


@anonymous_required
def auth_login(request, template="bootstrap3/account/auth_login.html", context={}):
    pass


@anonymous_required
def auth_register(request, template="bootstrap3/account/auth_register.html", context={}):
    pass


@anonymous_required
def auth_google(request, template="bootstrap3/account/auth_login.html", context={}):
    pass


@anonymous_required
def auth_facebook(request, template="bootstrap3/account/auth_facebook.html", context={}):
    pass


@anonymous_required
def auth_twitter(request, template="bootstrap3/account/auth_twitter.html", context={}):
    pass


@anonymous_required
def auth_logout(request, template="bootstrap3/account/auth_logout.html", context={}):
    pass

