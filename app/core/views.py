from django import http
from django.views.decorators.cache import cache_page
from django.utils.http import is_safe_url
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from core.logic import PageLogic

''' Default pages '''


def home(request, template='user/core/home.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 1)
def about(request, template='user/core/about.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


''' Error pages '''


@cache_page(60 * 60)
def error_400(request, template='user/core/error_400.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_403(request, template='user/core/error_403.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_404(request, template='user/core/error_404.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_500(request, template='user/core/error_500.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


''' Core pages '''


def language(request, code):
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    l = PageLogic(request)
    l.set_language(code, response=response)
    return response


@staff_member_required
def debug(request, template='user/core/debug.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)

