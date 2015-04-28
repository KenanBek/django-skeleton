from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from . import models


def store_user_request(request):
    if not settings.APPLICATION_MONITORING:
        return
    if not settings.APPLICATION_MONITOR_STUFF_USERS and request.user.is_staff:
        return
    user_request = models.Request()

    user_request.server_name = request.META.get('SERVER_NAME', '')
    user_request.server_host = request.META.get('HTTP_HOST', '')

    user_request.user_username = request.user.username
    user_request.user_is_staff = request.user.is_staff
    user_request.user_is_active = request.user.is_active

    user_request.client_name = request.META.get('USER', '')
    user_request.client_ip = request.META.get('REMOTE_ADDR', '')
    user_request.client_agent = request.META.get('HTTP_USER_AGENT', '')

    real_ip = get_real_ip(request)
    if real_ip is None:
        real_ip = get_ip(request)
    user_request.client_real_ip = real_ip

    user_request.scheme = request.scheme
    user_request.method = request.method
    user_request.data = request.REQUEST

    user_request.is_ajax = request.is_ajax()

    user_request.from_page = request.META.get('HTTP_REFERER', '')
    user_request.to_page = request.path
    user_request.to_page_query = request.META.get('QUERY_STRING', '')

    user_request.save()
    return user_request

