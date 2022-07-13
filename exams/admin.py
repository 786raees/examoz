from django.contrib import admin
from .models import Answer, Exam, Option, Question, Result, Course
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title','question','no_of_score','avg_score',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title','question_marks')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question','answer')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question','option',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('email','exam')