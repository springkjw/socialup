from django.utils.decorators import method_decorator
from .decorators import ajax_required


class AjaxRequireMixin(object):
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AjaxRequireMixin, self).dispatch(request, *args, **kwargs)