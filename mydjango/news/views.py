from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from django.template.loader import  render_to_string
from django.views.decorators.http import require_http_methods
# noinspection PyUnresolvedReferences
# from mydjango.utils import ajax_required
# Create your views here.
from django.views.generic import ListView
from mydjango.news.models import News



class NewsListView(ListView):
    """新闻列表页"""
    # model = News
    # queryset = News.objects.filter(reply=False).all()
    paginate_by = 10
    template_name = "news/news_list.html"
    content_object_name = 'news_list'

    def get_queryset(self, *kwargs):
        return News.objects.filter(reply=False).all()

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(NewsListView, self).get_context_data()
    #     context['importantNews'] = News
    #     return context

@login_required
# @ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """发送ajax post请求"""
    newsContent = request.POST['news_content'].strip()
    if newsContent:
        news = News.objects.create(user=request.user, content=newsContent)
        html = render_to_string('news/news_single.html', {'news': news, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空！")


