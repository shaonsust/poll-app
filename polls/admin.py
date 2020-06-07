"""
Django admin
"""

from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """
    Choice table
    """

    model = Choice
    extra = 0


# Creating custom Question admin here.
class QuestionAdmin(admin.ModelAdmin):
    """
    Question Admin area for crud operation.
    """

    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date", "question_text"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    """
    Choice Admin area for crud operation.
    """

    fields = ["question", "choice_text", "votes"]
    list_display = ("choice_text", "votes", "question")
    list_filter = ("choice_text", "votes", "question")
    search_fields = ("choice_text", "votes", "question")


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
