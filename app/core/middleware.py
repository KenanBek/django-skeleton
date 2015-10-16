from core.logic import ViewPage


class CoreMiddleware(object):
    def process_request(self, request):
        page_logic = ViewPage(request)
        page_logic.store_request()
        return None  # Continue processing request

