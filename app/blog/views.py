from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms as django_forms
from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _

from core.utils.decorators import log
from . import forms
from . import logic


@log
@cache_page(60 * 3)
def index(request, template='user/blog/index.html', context={}):
    blog_logic = logic.BlogViewPage(request)

    context['pages'] = blog_logic.pages()
    context['posts'] = blog_logic.posts()
    # context['beeps'] = blog_logic.beeps()
    return render(request, template, context)


''' Pages '''


@log
def pages(request, template='user/blog/pages.html', context={}):
    blog_logic = logic.BlogViewPage(request)
    context['pages'] = blog_logic.pages()
    return render(request, template, context)


@log
@cache_page(60 * 3)
def page(request, page_slug, template='user/blog/page.html', context={}):
    blog_logic = logic.BlogViewPage(request)
    context['page'] = blog_logic.page(page_slug)
    return render(request, template, context)


''' Posts '''


@log
def posts(request, template='user/blog/posts.html', context={}):
    blog_logic = logic.BlogViewPage(request)
    context['posts'] = blog_logic.posts()
    return render(request, template, context)


@log
@cache_page(60 * 3)
def post(request, post_id, post_slug, template='user/blog/post.html', context={}):
    blog_logic = logic.BlogViewPage(request)
    context['post'] = blog_logic.post(post_id, post_slug)
    return render(request, template, context)


''' Others '''


@log
def contact(request, template="user/blog/contact.html", context={}):
    contact_form = forms.ContactForm(request.POST or None)

    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(request, messages.SUCCESS, _('Your message successfully submitted.'))
            return redirect(reverse('blog_contact'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['contact_form'] = contact_form
    context['document_form'] = forms.DocumentForm()

    return render(request, template, context)


@log
def document(request, template="user/blog/contact.html", context={}):
    document_form = forms.DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if document_form.is_valid():
            document_form.save()
            messages.add_message(request, messages.SUCCESS, _('Your application successfully submitted.'))
            return redirect(reverse('blog_contact'))
        else:
            messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))

    context['contact_form'] = forms.ContactForm()
    context['document_form'] = document_form

    return render(request, template, context)


@log
def search(request, template='user/blog/search.html', context={}):
    blog_logic = logic.BlogViewPage(request)

    term = blog_logic.get_param("term")
    search_result = blog_logic.search(term)

    context['term'] = term
    context['pages'] = search_result.pages
    context['posts'] = search_result.posts
    return render(request, template, context)


@log
def subscribe(request):
    blog_logic = logic.BlogViewPage(request)

    name = blog_logic.get_param("name")
    email = blog_logic.get_param("email")

    if not name or not email:
        messages.add_message(request, messages.ERROR, _('Please enter your name and email.'))
    else:
        try:
            django_forms.EmailField().clean(email)
            blog_logic.new_subscription(name, email)
            messages.add_message(request, messages.SUCCESS, _('You successfully subscribed.'))
        except ValidationError:
            messages.add_message(request, messages.ERROR, _('Please enter correct email.'))
        except IntegrityError:
            messages.add_message(request, messages.WARNING, _('You already have been subscribed.'))

    return redirect(request.META.get('HTTP_REFERER'))

