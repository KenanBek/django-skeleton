from django.conf import settings


def general(request, context={}):
    context['core_config'] = settings
    context['application_config'] = settings.APPLICATION_CONFIG
    return context

