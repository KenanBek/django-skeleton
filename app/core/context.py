from django.conf import settings

from .utils import helpers


def general(request, context={}):
    context['core_config'] = settings
    context['application_config'] = settings.APPLICATION_CONFIG
    context['application_settings'] = request.core_logic.settings_manager.get_dict()
    if request.method == 'GET':
        context['get_request_params'] = helpers.get_dict_as_request_params(request.GET)
    return context

