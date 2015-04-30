from django.shortcuts import render
from django.views.decorators.cache import cache_page


''' Default pages '''


def home(request, template='user/core/home.html', context={}):
    return render(request, template, context)


@cache_page(60 * 1)
def about(request, template='user/core/about.html', context={}):
    return render(request, template, context)


''' Error pages '''


@cache_page(60 * 60)
def error_400(request, template='user/core/error_400.html', context={}):
    return render(request, template, context)


@cache_page(60 * 60)
def error_403(request, template='user/core/error_403.html', context={}):
    return render(request, template, context)


@cache_page(60 * 60)
def error_404(request, template='user/core/error_404.html', context={}):
    return render(request, template, context)


@cache_page(60 * 60)
def error_500(request, template='user/core/error_500.html', context={}):
    return render(request, template, context)


''' Core pages '''


def debug(request, template='user/core/debug.html', context={}):
    return render(request, template, context)

