from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from . import logic


class CoreMiddleware(object):
    def process_request(self, request):
        # Set user's IP address
        local_ip = request.META.get('REMOTE_ADDR', '')
        request.user.local_ip = local_ip
        global_ip = get_real_ip(request)
        if global_ip is None:
            global_ip = get_ip(request)
        request.user.global_ip = global_ip

        # Set CoreLogic instance
        core_logic = logic.CoreLogic(request)
        request.core_logic = core_logic
        # Auto-store request
        if settings.APPLICATION_MONITORING:
            if not request.user.is_staff or (request.user.is_staff and settings.APPLICATION_MONITOR_STUFF_USERS):
                core_logic.store_request()
        return

