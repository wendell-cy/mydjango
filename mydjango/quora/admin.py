from django.contrib import admin

# Register your models here.
from mydjango.quora.models import Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    # list_editable = ['catname']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title', 'user', 'status', 'tags', 'created_at']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
