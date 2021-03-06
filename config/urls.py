from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # path("news/", TemplateView.as_view(template_name="pages/news.html"), name="news"),
    # path("blogs/", TemplateView.as_view(template_name="pages/blogs.html"), name="blogs"),
    # path("quora/", TemplateView.as_view(template_name="pages/quora.html"), name="quora"),
    path("chat/", TemplateView.as_view(template_name="pages/chat.html"), name="chat"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    ### 第三方路由
    re_path(r'mdeditor/', include('mdeditor.urls')),
    re_path(r'comments/', include('django_comments.urls')),
    # User management
    path("users/", include("mydjango.users.urls", namespace="users")),
    path("news/", include("mydjango.news.urls", namespace="news")),
    path("blogs/", include("mydjango.blogs.urls", namespace="blogs")),
    path("quora/", include("mydjango.quora.urls", namespace="quora")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
