from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

import forms


def index(request, template="bootstrap3/account/index.html", context={}):
    return render(request, template, context)


def register(request, template="bootstrap3/account/register.html", context={}):
    user_form = forms.UserForm(request.POST or None)
    profile_form = forms.ProfileForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.add_message(request, messages.INFO, 'You have successfully registered.')
            return redirect(reverse('account_index'))
        else:
            messages.add_message(request, messages.WARNING, 'Please fix errors bellow.')

    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['forms'] = (user_form, profile_form, )

    return render(request, template, context)

