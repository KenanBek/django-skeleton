from django.shortcuts import render


def index(request, template='home/index.html', context={}):
    return render(request, template, context)

