from django.shortcuts import render


def error_400(request, template='bootstrap3/error/error_400.html', context={}):
    return render(request, template, context)


def error_403(request, template='bootstrap3/error/error_403.html', context={}):
    return render(request, template, context)


def error_404(request, template='bootstrap3/error/error_404.html', context={}):
    return render(request, template, context)


def error_500(request, template='bootstrap3/error/error_500.html', context={}):
    return render(request, template, context)

