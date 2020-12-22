from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models import Count

from taggit.managers import TaggableManager


class ArticleCategory(models.Model):
    """定义文章类型"""
    catname = models.CharField(max_length=50, verbose_name="类别名称")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.catname

    class Meta:
        verbose_name = "文章类别"
        verbose_name_plural = verbose_name


class ArticleQuerySet(models.query.QuerySet):
    """自定义queryset ，提高模型的可用性"""

    def get_published(self):
        """返回已发表的文章"""
        return self.filter(status="P").order_by('_created_at')

    def get_drafts(self):
        """返回草稿箱的文章"""
        return self.filter(status="D").order_by('_updated_at')

    def get_counted_tag(self):
        """返回已发表的文章中，每一个标签的数量(大于0的)"""
        tag_dict ={}
        query = self.filter(status="P").annotate(tagged=Count('tags')).filter(tags__gt=0)


class Article(models.Model):
    STATUS = (("D", "Draft"), ("P", "Published"))
    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name="状态")
    category = models.ForeignKey(ArticleCategory, verbose_name="文章类别",
                                 null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,related_name="author",
                             on_delete=models.SET_NULL, verbose_name="作者")
    title = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name="文章标题")
    cover = models.ImageField(upload_to="blogs/covers/%y/%m/%d", verbose_name="文章封面")
    abstract = models.CharField(max_length=255, null=True, blank=True, verbose_name="文章摘要", default="此文章还没有摘要")
    content = models.TextField(verbose_name="文章内容")
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name="(url)别名")
    tags = TaggableManager(help_text="多个标签使用英文逗号(,)隔开", verbose_name="文章标签")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


