from django.contrib import messages
from django.http import HttpResponseRedirect

from django.shortcuts import render

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
    try:
        logic.subscribe(name, email)
        messages.add_message(request, messages.INFO, 'You successfully subscribed.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, 'Email is not unique.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


