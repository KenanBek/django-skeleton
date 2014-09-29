from django.contrib import messages

from django.shortcuts import render, redirect

import forms

import logic


def index(request, template='bootstrap3/website/index.html', context={}):
    pages = logic.load_pages()
    posts = logic.load_posts()

    context['pages'] = pages
    context['posts'] = posts
    return render(request, template, context)


def features(request, template='bootstrap3/website/features.html', context={}):
    return render(request, template, context)


def about(request, template='bootstrap3/website/about.html', context={}):
    return render(request, template, context)


def page(request, page_slug, template='bootstrap3/website/page.html', context={}):
    context['page'] = logic.get_page(page_slug)
    return render(request, template, context)


def post(request, post_id, post_slug, template='bootstrap3/website/post.html', context={}):
    context['post'] = logic.get_post(post_id, post_slug)
    return render(request, template, context)


def search(request, template='bootstrap3/website/search.html', context={}):
    term = request.GET['term']
    search_result = logic.search(term)

    context['term'] = term
    context['pages'] = search_result.pages
    context['posts'] = search_result.posts
    return render(request, template, context)


def subscribe(request):
    name = request.GET['name']
    email = request.GET['email']

    if not email:
        messages.add_message(request, messages.WARNING, 'Please enter your email.')
    else:
        try:
            logic.subscribe(name, email)
            messages.add_message(request, messages.INFO, 'You successfully subscribed.')
        except Exception as e:
            messages.add_message(request, messages.WARNING, 'You already have been subscribed.')
    return redirect(request.META.get('HTTP_REFERER'))


def contact(request, template="bootstrap3/website/contact.html", context={}):
    contact_form = forms.ContactForm(request.POST or None)

    if request.method == 'POST':
        if contact_form.is_valid():
            contact_form.save()
            messages.add_message(request, messages.INFO, 'Your message successfully submitted.')
            return redirect('/contact')
        else:
            messages.add_message(request, messages.WARNING, 'Please fix errors bellow.')

    context['contact_form'] = contact_form
    context['document_form'] = forms.DocumentForm()

    return render(request, template, context)


def document(request, template="bootstrap3/website/contact.html", context={}):
    document_form = forms.DocumentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if document_form.is_valid():
            document_form.save()
            messages.add_message(request, messages.INFO, 'Your application successfully submitted.')
            return redirect('/contact')
        else:
            messages.add_message(request, messages.WARNING, 'Please fix errors bellow.')

    context['contact_form'] = forms.ContactForm()
    context['document_form'] = document_form

    return render(request, template, context)

