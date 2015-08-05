from django.contrib.admin.views.decorators import staff_member_required

from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from core.logic import PageLogic

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


def language(request, code):
    l = PageLogic(request)
    l.set_language(code)
    if request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse('home'))


@staff_member_required
def debug(request, template='user/core/debug.html', context={}):
    return render(request, template, context)

