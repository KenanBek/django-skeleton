from django.conf import settings


def general(request, context={}):
    context['core_config'] = settings
    context['application_config'] = settings.APPLICATION_CONFIG
    context['application_settings'] = request.core_logic.settings_manager.get_dict()
    return context

