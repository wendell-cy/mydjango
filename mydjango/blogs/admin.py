from django.contrib import admin

# Register your models here.
from mydjango.blogs.models import Article, ArticleCategory


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['catname', 'created_at', 'updated_at']
    # list_editable = ['catname']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'user', 'category', 'status', 'tags', 'created_at']


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
