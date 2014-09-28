from django.shortcuts import render
from models import Page, Post


def index(request, template='bootstrap3/website/index.html', context={}):
    pages = Page.objects.all()
    posts = Post.objects.all()

    context['pages'] = pages
    context['posts'] = posts
    return render(request, template, context)


def features(request, template='bootstrap3/website/features.html', context={}):
    return render(request, template, context)


def about(request, template='bootstrap3/website/about.html', context={}):
    return render(request, template, context)


def page(request, page_slug, template='bootstrap3/website/page.html', context={}):
    page_item = Page.objects.get(slug=page_slug)

    context['page'] = page_item
    return render(request, template, context)


def post(request, post_id, post_slug, template='bootstrap3/website/post.html', context={}):
    post_item = Post.objects.get(pk=post_id, slug=post_slug)

    context['post'] = post_item
    return render(request, template, context)

