
from django.utils import translation


class LocaleMiddleware(object):
    def process_request(self, request):
        language = translation.get_language_from_request(request)

        if request.user.is_authenticated() and request.user.profile.language:
            language = request.user.profile.language

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
