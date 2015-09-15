from core.logic import PageLogic


class CoreMiddleware(object):
    def process_request(self, request):
        page_logic = PageLogic(request)
        page_logic.store_request()
        return None  # Continue processing request

