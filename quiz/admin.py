from django.contrib import admin
from .models import Subject, Question

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "grade", "subject", "correct", "text_short", "created_at")
    list_filter = ("grade", "subject", "correct")
    search_fields = ("text", "option_a", "option_b", "option_c", "option_d")

    def text_short(self, obj: Question):
        return (obj.text[:60] + "...") if len(obj.text) > 60 else obj.text
    text_short.short_description = "Savol"

from .models import Subject, Question, TestAttempt, TestAnswer

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "grade", "subject", "correct", "wrong", "total", "created_at")
    list_filter = ("grade", "subject")
    search_fields = ("user__username",)

@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "attempt", "question", "selected", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("attempt__user__username",)
