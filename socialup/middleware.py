from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.models import Site
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


class SiteMiddleware(object):
    def process_request(self, request):
        try:
            current_site = Site.objects.get(domain=request.get_host())
        except Site.DoesNotExist:
            current_site = Site.objects.get(id=settings.DEFAULT_SITE_ID)

        request.current_site = current_site
        settings.SITE_ID = current_site.id
