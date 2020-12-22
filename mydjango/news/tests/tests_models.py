# from django.test import TestCase
from mydjango.news.models import News
from test_plus import TestCase
# Create your tests here.

class NewsModelsTest(TestCase):

    def setUp(self):
        self.user1 = self.make_user(username="user1", password="xxxxx")
        self.user2 = self.make_user(username="user2", password="ooooooo")
        self.news1 = News.objects.create(user=self.user1, content="第一条新闻")
        self.news2 = News.objects.create(user=self.user2, content="第二条新闻")
        self.news3 = News.objects.create(user=self.user1, content="回复第一条新闻", reply=True, parent=self.news1)

    def test__str__(self):
        self.assertEqual(self.news1.__str__(), "第一条新闻")

    def test_switch_like(self):
        self.news1.switch_like(self.user2)
        assert self.news1.likers_count() == 1
        self.news1.switch_like(self.user1)
        assert self.news1.likers_count() == 2
        assert self.user1 in self.news1.get_likers()
        assert self.user2 in self.news1.get_likers()
        self.news1.switch_like(self.user1)
        assert self.user1 not in self.news1.get_likers()
        assert self.news1.likers_count() == 1

    def test_reply_this(self):
        initial_count = News.objects.count()
        self.news1.reply_this(self.user2, "第二次回复第一条新闻")
        assert News.objects.count() == initial_count + 1
        assert self.news1.replies_count() == 2
        assert self.news3 in self.news1.get_children()
