from django.shortcuts import render

from core.decorators import convert_to_json


@convert_to_json
def request_info(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # Get custom set
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # Prepare result variable
    info = {
        "GET": request.GET,
        "POST": request.POST,
        "REQUEST": request.REQUEST,
        "COOKIES": request.COOKIES,
        "META": request.META,
        "body": request.body,
        "environ": request.environ,
        "encoding": request.encoding,
        "method": request.method,
        "path": request.path,
        "path_info": request.path_info,
        "session": request.session,
        "user": request.user,
        "scheme": request.scheme,
        "custom_set_ip": ip,
    }
    return info


def localization_info(request, template='user/system/localization.html', context={}):
    return render(request, template, context)

