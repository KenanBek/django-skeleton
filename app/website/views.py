from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django import forms as django_forms
import markdown2

import forms
import logic


def index(request, template='user/website/index.html', context={}):
    pages = logic.load_pages()
    posts = logic.load_posts()

    context['pages'] = pages
    context['posts'] = posts
    return render(request, template, context)


def about(request, template='user/website/about.html', context={}):
    context['about_text'] = markdown2.markdown_path("readme.md")
    return render(request, template, context)


def contact(request, template="user/website/contact.html", context={}):
    contact_form = forms.ContactForm(request.POST or None)

    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(request, messages.SUCCESS, _('Your message successfully submitted.'))
            return redirect(reverse('website_contact'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['contact_form'] = contact_form
    context['document_form'] = forms.DocumentForm()

    return render(request, template, context)


def document(request, template="user/website/contact.html", context={}):
    document_form = forms.DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if document_form.is_valid():
            document_form.save()
            messages.add_message(request, messages.SUCCESS, _('Your application successfully submitted.'))
            return redirect(reverse('website_contact'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['contact_form'] = forms.ContactForm()
    context['document_form'] = document_form

    return render(request, template, context)


def search(request, template='user/website/search.html', context={}):
    q = request.GET.get('q', False)
    search_result = logic.search(q)

    context['q'] = q
    context['pages'] = search_result.pages
    context['posts'] = search_result.posts
    return render(request, template, context)


def subscribe(request):
    name = request.GET.get('name', False)
    email = request.GET.get('email', False)

    if not name or not email:
        messages.add_message(request, messages.ERROR, _('Please enter your name and email.'))
    else:
        try:
            django_forms.EmailField().clean(email)
            logic.subscribe(name, email)
            messages.add_message(request, messages.SUCCESS, _('You successfully subscribed.'))
        except ValidationError:
            messages.add_message(request, messages.ERROR, _('Please enter correct email.'))
        except IntegrityError:
            messages.add_message(request, messages.WARNING, _('You already have been subscribed.'))

    return redirect(request.META.get('HTTP_REFERER'))


def page(request, page_slug, template='user/website/page.html', context={}):
    context['page'] = logic.get_page(page_slug)
    return render(request, template, context)


@login_required
def post(request, post_id, post_slug, template='user/website/post.html', context={}):
    context['post'] = logic.get_post(post_id, post_slug)
    return render(request, template, context)

