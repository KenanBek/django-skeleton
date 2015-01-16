from django.shortcuts import render

''' Error pages '''


def error_400(request, template='bootstrap3/system/error_400.html', context={}):
    return render(request, template, context)


def error_403(request, template='bootstrap3/system/error_403.html', context={}):
    return render(request, template, context)


def error_404(request, template='bootstrap3/system/error_404.html', context={}):
    return render(request, template, context)


def error_500(request, template='bootstrap3/system/error_500.html', context={}):
    return render(request, template, context)

