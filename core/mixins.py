from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator


class FormValidRedirectMixing(object):
    def success_redirect(self, message):
        messages.success(self.request, message)
        return HttpResponseRedirect(self.get_success_url())


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
