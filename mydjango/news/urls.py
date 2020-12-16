from django.urls import path

from mydjango.news import views

app_name = "news"

urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
    path("post-news/", views.post_news, name="post_news"),
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # # path("<str:username>/", view=user_detail_view, name="detail"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
