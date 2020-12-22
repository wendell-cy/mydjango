from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views import View


def ajax_required(f):
    """验证是否为ajax请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        #  request.is_ajax()
        if not request.is_ajax():
            return HttpResponseBadRequest('不是ajax请求')
        return f(request, *args, **kwargs)
    return wrap

class AuthorRequiredMixin(View):
    """验证是否为原作者，用于删除和文章编辑"""
    def dispatch(self, request, *args, **kwargs):
        # 状态和文章案例有user属性
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
