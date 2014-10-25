from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation


def localization(request, template='bootstrap3/system/localization.html', context={}):
    return render(request, template, context)

"""
def language(request, lang):
    translation.activate(lang)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
"""

