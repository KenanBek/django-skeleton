from core.decorators import json, anonymous_required


@anonymous_required
@json
def login(request):
    if request.is_ajax():
        return request.body

    return "boom"