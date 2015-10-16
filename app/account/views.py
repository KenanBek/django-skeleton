from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import django.contrib.auth as django_auth
import hashlib
import datetime
import random
from account.models import REQUEST_TYPE_ACCOUNT, REQUEST_TYPE_EMAIL, REQUEST_TYPE_PASSWORD
from core.settings import APPLICATION_URL, APPLICATION_FROM_EMAIL
from django.utils import timezone
from core.utils.decorators import log, anonymous_required
from . import models
from . import forms


def index(request, template="user/account/index.html", context={}):
    return render(request, template, context)


@log
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
                        return redirect(reverse('home'))
                else:
                    messages.add_message(request, messages.WARNING, _('Non active user.'))
            else:
                messages.add_message(request, messages.ERROR, _('Wrong username or password.'))

    context['login_form'] = login_form
    return render(request, template, context)


@log
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
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt+user_email).hexdigest()
                key_expires_at = datetime.datetime.today() + datetime.timedelta(2)
                models.Request.objects.create(user=user, type=REQUEST_TYPE_ACCOUNT,
                                              activation_key=activation_key, key_expires_at=key_expires_at)
                email_subject = _('Account confirmation')
                email_body = _("Hey mate, thanks for signing up. To activate your account, click this link within 48hours\n") + \
                    APPLICATION_URL + reverse('account_request_confirm', args=(activation_key,))
                send_mail(email_subject, email_body, APPLICATION_FROM_EMAIL, [user_email], fail_silently=False)

                return redirect(reverse('account_index'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)


def request_confirm(request, activation_key, template='user/account/password_reset.html', context={}):
    user_request = get_object_or_404(models.Request, activation_key=activation_key)

    if user_request.is_approved or user_request.key_expires_at < timezone.now():
        return render_to_response('user/account/token_invalid.html')
    elif user_request.type == REQUEST_TYPE_ACCOUNT:
        profile = get_object_or_404(models.Profile, user=user_request.user)
        profile.is_verified = True
        profile.save()
        user_request.is_approved = True
        user_request.save()
        return render_to_response('user/account/confirm.html')
    elif user_request.type == REQUEST_TYPE_EMAIL:
        user = User.objects.get(id=user_request.user.id)
        user.email = user_request.str_field_1
        user.save()
        profile = get_object_or_404(models.Profile, user=request.user)
        profile.is_verified = True
        profile.save()
        user_request.is_approved = True
        user_request.save()
        return render_to_response('user/account/confirm.html')
    elif user_request.type == REQUEST_TYPE_PASSWORD:
        if request.method == 'POST':
            reset_password_form = forms.ResetPasswordForm(request.POST or None)
            if reset_password_form.is_valid():
                new_password = str(reset_password_form.cleaned_data['new_password'])
                repeat_new_password = str(reset_password_form.cleaned_data['repeat_new_password'])
                if new_password == repeat_new_password:
                    user = user_request.user
                    user.set_password(new_password)
                    user.save()
                    django_auth.logout(request)
                    messages.add_message(request, messages.SUCCESS, _('You have successfully changed your password.'
                                                                      '\nPlease, log in now.'))
                    user_request.is_approved = True
                    user_request.str_field_2 = new_password
                    user_request.save()
                    return redirect(reverse('home'))
                else:
                    messages.add_message(request, messages.ERROR, _('Passwords are not matching.'
                                                                    '\nPlease type them again.'))
        else:
            reset_password_form = forms.ResetPasswordForm()
        context['reset_password_form'] = reset_password_form
        return render(request, template, context)
    else:
        return render_to_response('user/account/token_invalid.html')


@log
@login_required
def logout(request):
    django_auth.logout(request)
    messages.add_message(request, messages.SUCCESS, _('You have successfully logged out.'))
    return redirect(reverse('home'))


@log
@login_required
def change_password(request, template="user/account/password_change.html", context={}):
    change_password_form = None

    if request.method == 'POST':
        change_password_form = forms.ChangePasswordForm(request.POST or None)
        if change_password_form.is_valid():
            user = request.user
            if change_password_form.cleaned_data['new_password'] == change_password_form.cleaned_data['repeat_new_password']:
                if user.check_password(change_password_form.cleaned_data['current_password']):
                    user.set_password(change_password_form.cleaned_data['new_password'])
                    user.save()
                    django_auth.logout(request)
                    messages.add_message(request, messages.SUCCESS, _('You have successfully changed your password.'
                                                                      '\nPlease, log in again.'))
                    return redirect(reverse('home'))
                else:
                    messages.add_message(request, messages.ERROR, _('Current password is wrong.'
                                                                    '\nPlease type it again.'))
            else:
                messages.add_message(request, messages.ERROR, _('Passwords are not matching.'
                                                                '\nPlease type them again.'))
        else:
            messages.add_message(request, messages.ERROR, _('Some errors occurred.'
                                                            '\nPlease fix errors bellow.'))
    else:
        change_password_form = forms.ChangePasswordForm()

    context['change_password_form'] = change_password_form

    return render(request, template, context)


@log
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
            messages.add_message(request, messages.ERROR, _('Some errors occurred.'
                                                            '\nPlease fix errors bellow.'))
    else:
        user = request.user
        user_form = forms.ModifyUserForm(instance=user)
        profile_form = forms.ModifyProfileForm(instance=user.profile)

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)


@log
def restore_password(request, template="user/account/password_restore.html", context={}):
    restore_password_form = None

    if request.method == 'POST':
        restore_password_form = forms.RestorePasswordForm(request.POST or None)
        if restore_password_form.is_valid():
            try:
                user = User.objects.get(email=str(restore_password_form.cleaned_data['email']))
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                activation_key = hashlib.sha1(salt+user.email).hexdigest()
                key_expires_at = datetime.datetime.today() + datetime.timedelta(2)

                user_request, created = models.Request.objects.update_or_create(
                    user=user, type=REQUEST_TYPE_PASSWORD,
                    defaults={"activation_key": hashlib.sha1(salt+user.email).hexdigest(),
                              "key_expires_at": datetime.datetime.today() + datetime.timedelta(2)})

                # Send email with activation key
                email_subject = _('Password restore')
                email_body = _("Hey mate, forgot password? To reset your password, click this link within 48hours\n") +\
                    APPLICATION_URL + reverse('account_request_confirm', args=(activation_key,))

                send_mail(email_subject, email_body, APPLICATION_FROM_EMAIL, [user.email], fail_silently=False)
                messages.add_message(request, messages.SUCCESS, _('Email with instructions successfully sent.'))
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, _('No account with specified email found!'))
                return redirect(reverse('account_restore_password'))
        else:
            messages.add_message(request, messages.ERROR, _('Some errors occurred.'
                                                            '\nPlease fix errors bellow.'))
    else:
        if request.user.is_authenticated():
            restore_password_form = forms.RestorePasswordForm({'email': request.user.email})
        else:
            restore_password_form = forms.RestorePasswordForm()

    context['restore_password_form'] = restore_password_form

    return render(request, template, context)


@log
@login_required
def change_email(request, template="user/account/email_change.html", context={}):
    change_email_form = None

    if request.method == 'POST':
        change_email_form = forms.ChangeEmailForm(request.POST or None)
        if change_email_form.is_valid():
            user = User.objects.get(id=request.user.id)
            new_email = change_email_form.cleaned_data['email']
            if new_email and User.objects.filter(email=new_email).count():
                messages.add_message(request, messages.ERROR, _('User with this Email already exists.'))
                return redirect(reverse('account_change_email'))
            if new_email != user.email:
                user.profile.is_verified = False
                user.profile.save()
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                user_request, created = models.Request.objects.update_or_create(
                    user=user, type=REQUEST_TYPE_EMAIL,
                    defaults={"str_field_1": new_email,
                              "str_field_2": user.email,
                              "activation_key": hashlib.sha1(salt+new_email).hexdigest(),
                              "key_expires_at": datetime.datetime.today() + datetime.timedelta(2)})
                # Send email with activation key
                email_subject = _('Email change confirmation')
                email_body = _("Hey mate. To activate your new email, click this link within 48hours\n") + \
                    APPLICATION_URL + reverse('account_request_confirm', args=(user_request.activation_key,))

                send_mail(email_subject, email_body, APPLICATION_FROM_EMAIL, [new_email], fail_silently=False)
                return redirect(reverse('home'))
            else:
                messages.add_message(request, messages.ERROR, _('Email entered is the same as your current email.'))
        else:
            messages.add_message(request, messages.ERROR, _('Some errors occurred.'
                                                            '\nPlease fix errors bellow.'))
    else:
        change_email_form = forms.ChangeEmailForm()

    context['change_email_form'] = change_email_form

    return render(request, template, context)
