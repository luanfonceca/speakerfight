
from django.utils import translation


class LocaleMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        language = translation.get_language_from_request(request)

        if request.user.is_authenticated and request.user.profile.language:
            language = request.user.profile.language

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
