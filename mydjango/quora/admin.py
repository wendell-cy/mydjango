from django.contrib import admin

# Register your models here.
from mydjango.quora.models import Question, Answer, Vote


class VoteAdmin(admin.ModelAdmin):
    list_display = ['uuid_id', 'user', 'value', 'content_type', 'object_id', 'vote']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['uuid_id', 'user', 'question', 'is_accepted']
    # list_editable = ['catname']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'slug', 'status', 'tags', 'has_correct']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Vote, VoteAdmin)
