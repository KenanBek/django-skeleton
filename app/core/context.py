from django.conf import settings

def general(request, context={}):
    context['skeleton_config'] = settings.SKELETON_CONFIG
    return context