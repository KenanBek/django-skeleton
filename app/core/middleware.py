from ipware.ip import get_real_ip, get_ip


class CoreMiddleware(object):
    def process_request(self, request):
        # Get user's IP address
        ip = get_real_ip(request)
        if ip is None:
            ip = get_ip(request)
        request.user.ip = ip

        return

