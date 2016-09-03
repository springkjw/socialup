from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXCEPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXECPT_URLS'):
    EXCEPT_URLS += [compile(expr) for expr in settings.LOGIN_EXECPT_URLS]


class LoginRequireMiddleware:
    def process_request(self, request):
        assert hasattr(request, 'user')

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXCEPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)