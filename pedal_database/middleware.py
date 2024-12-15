from django.http import HttpResponsePermanentRedirect

class WWWRedirectMiddleware:
    """
    Middleware to redirect non-www requests to www.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == "guitarpedaldb.com":
            return HttpResponsePermanentRedirect(f"https://www.guitarpedaldb.com{request.get_full_path()}")
        return self.get_response(request)
