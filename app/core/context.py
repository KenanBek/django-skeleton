from django.conf import settings

from core.logic import ViewPage
from .utils import helpers


def general(request):
    context = {
        'core_config': settings,
        'application_config': settings.APPLICATION_CONFIG
    }

    page_logic = ViewPage(request)
    context['application_settings'] = page_logic.settings_manager.get_dict()
    for k, v in enumerate(page_logic.context):
        context[v] = page_logic.context[v]

    if request.method == 'GET':
        context['request_get_params'] = helpers.get_dict_as_request_params(request.GET)
    return context

