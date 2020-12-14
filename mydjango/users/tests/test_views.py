# import pytest
# from django.contrib.auth.models import AnonymousUser
# from django.http.response import Http404
# from django.test import RequestFactory
#
# from mydjango.users.models import User
# from mydjango.users.tests.factories import UserFactory
# from mydjango.users.views import (
#     UserRedirectView,
#     UserUpdateView,
#     user_detail_view,
# )
#
# pytestmark = pytest.mark.django_db
#
#
# class TestUserUpdateView:
#     """
#     TODO:
#         extracting view initialization code as class-scoped fixture
#         would be great if only pytest-django supported non-function-scoped
#         fixture db access -- this is a work-in-progress for now:
#         https://github.com/pytest-dev/pytest-django/pull/258
#     """
#
#     def test_get_success_url(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_success_url() == f"/users/{user.username}/"
#
#     def test_get_object(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_object() == user
#
#
# class TestUserRedirectView:
#     def test_get_redirect_url(self, user: User, rf: RequestFactory):
#         view = UserRedirectView()
#         request = rf.get("/fake-url")
#         request.user = user
#
#         view.request = request
#
#         assert view.get_redirect_url() == f"/users/{user.username}/"
#
#
# class TestUserDetailView:
#     def test_authenticated(self, user: User, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = UserFactory()
#
#         response = user_detail_view(request, username=user.username)
#
#         assert response.status_code == 200
#
#     def test_not_authenticated(self, user: User, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = AnonymousUser()
#
#         response = user_detail_view(request, username=user.username)
#
#         assert response.status_code == 302
#         assert response.url == "/accounts/login/?next=/fake-url/"
#
#     def test_case_sensitivity(self, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = UserFactory(username="UserName")
#
#         with pytest.raises(Http404):
#             user_detail_view(request, username="username")
from django.urls import reverse,resolve
from test_plus import TestCase


class TestUserUrls(TestCase):
    def setUp(self):
        self.user = self.make_user(username='testuser', password='password')

    def test_detail_reverse(self):
        reverse_url = reverse("users:detail", kwargs={"username": self.user.username})
        self.assertEqual(reverse_url, f"/users/{self.user.username}/")

    def test_detail_resolve(self):
        resolve_urlname = resolve(f"/users/{self.user.username}/").view_name
        self.assertEqual(resolve_urlname, "users:detail")

    def test_update_reverse(self):
        reverse_url = reverse("users:update")
        self.assertEqual(reverse_url, "~update/")

    def test_update_resolve(self):
        resolve_urlname = resolve("~update/").view_name
        self.assertEqual(resolve_urlname, "users:update")

    def test_redirect_reverse(self):
        reverse_url = reverse("users:redirect")
        self.assertEqual(reverse_url, "~redirect/")

    def test_redirect_resolve(self):
        resolve_urlname = resolve("~redirect/").view_name
        self.assertEqual(resolve_urlname, "users:redirect")
