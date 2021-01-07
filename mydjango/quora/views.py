from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from mydjango.quora.models import Question


class QuestionListView(ListView):
    """所有问题列表"""
    model = Question
    paginate_by = 20
    context_object_name = 'questions-list'
    template_name = 'quora/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context["popular_tags"] = Question.objects.get_counted_tag()
        return context

class CorrectAnsweredQuestionListView(QuestionListView):
    """已有采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_correct_answered()

class UncorrectAnsweredQuestionListView(QuestionListView):
    """还没有被采纳答案的问题列表"""
    def get_queryset(self):
        return Question.objects.get_uncoreect_answered()
