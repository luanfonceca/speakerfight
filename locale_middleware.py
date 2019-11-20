
from django.utils import translation


class LocaleMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self, request):
        language = translation.get_language_from_request(request)

        if request.user.is_authenticated and request.user.profile.language:
            language = request.user.profile.language

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
