# from django.test import TestCase
from django.test import Client
from mydjango.news.models import News
from test_plus import TestCase
# Create your tests here.

class NewsViewsTest(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.client = Client()
        self.other_client = Client()

        self.client.login(username="user01", password="password")

        self.first_news = News.objects.create(
            user=self.user,
            content="第一条动态"
        )

        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )

        self.third_news = News.objects.create(
            user=self.other_user,
            content="第三条条动态",
            reply=True,
            parent=self.first_news
        )
