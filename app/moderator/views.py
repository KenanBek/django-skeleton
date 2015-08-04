from django.shortcuts import render


def index(request, template='moderator/common/index.html'):
    context = {}
    return render(request, template, context)

