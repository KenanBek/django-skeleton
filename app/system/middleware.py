from system import logic


class SystemMiddleware(object):
    def process_request(self, request):
        logic.store_user_request(request)
        return

