from django.contrib import admin
from .models import Exam
# Register your models here.

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title','question','no_of_score','avg_score',)