from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from django.template.loader import  render_to_string
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
# noinspection PyUnresolvedReferences
from mydjango.utils import ajax_required, AuthorRequiredMixin
# Create your views here.
from django.views.generic import ListView, DeleteView
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
@ajax_required
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

class NewDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """删除一条新闻记录"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news:list')

@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    """点赞，相应ajax post请求"""
    news_id = request.POST['newsId']
    news = News.objects.get(pk=news_id)
    # 取消或者添加点赞
    news.switch_like(request.user)
    # 返回点赞数量
    return JsonResponse({"liker_count": news.likers_count()})

@login_required
@ajax_required
@require_http_methods(['POST'])
def post_reply(request):
    """发送回复ajax post请求"""
    print(request.POST['replyContent'])
    replyContent = request.POST['replyContent'].strip()
    parentId = request.POST['newsid']
    parent = News.objects.get(pk=parentId)
    # print(replyContent)
    if replyContent:
        parent.reply_this(request.user, replyContent)
        return JsonResponse({"newsid": parent.pk, "replies_count": parent.replies_count()})
    else:
        return HttpResponseBadRequest("内容不能为空！")

@ajax_required
@require_http_methods(['POST', 'GET'])
def get_replies(request):
    """返回新闻的评论"""
    news_id = request.GET['newsId']
    news = News.objects.get(pk=news_id)
    # render_to_string() 表示加载模板 填充数据，返回字符串
    replies_html = render_to_string("news/reply_list.html", {"replies": news.get_children()})
    # print(replies_html)
    return JsonResponse({
        "uuid": news_id,
        "replies_html": replies_html,
    })
