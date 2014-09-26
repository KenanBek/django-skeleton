from django.shortcuts import render

from core.decorators import use_theme


@use_theme("bootstrap3")
def index(request, template='website/index.html', context={}):
    return render(request, template, context)

