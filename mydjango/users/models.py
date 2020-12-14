from django.contrib.auth.models import AbstractUser
# from django.db.models import CharField
from django.db import models
from django.urls import reverse

# from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class User(AbstractUser):
    """Default user for mydjango."""

    #: First and last name do not cover name patterns around the globe
    # name = CharField(_("Name of User"), blank=True, max_length=255)
    nickname = models.CharField(verbose_name='用户昵称', blank=True, null=True, max_length=255,default='')
    job = models.CharField(verbose_name='用户职业', blank=True, null=True, max_length=50, default='未知')
    introduction = models.TextField(blank=True, null=True, verbose_name='简介', default='该用户很懒，啥也没写')
    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True, verbose_name='用户头像',default='')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='住址', default='')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日', default=timezone.now)
    personal_url = models.URLField(max_length=50, null=True, blank=True, verbose_name='个人链接', default='')
    weibo = models.URLField(max_length=50, null=True, blank=True, verbose_name='微博链接', default='')
    zhihu = models.URLField(max_length=50, null=True, blank=True, verbose_name='知乎链接', default='')
    github = models.URLField(max_length=50, null=True, blank=True, verbose_name='GitHub链接', default='')
    linkedin = models.URLField(max_length=50, null=True, blank=True, verbose_name='LinkedIn链接', default='')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username

    def get_absolute_url(self):
        return reverse("user:detail", kwargs={"username", self.username})

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
