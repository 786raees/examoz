from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from .models import Exam
# Create your views here.

class ExamList(LoginRequiredMixin,ListView):
    model = Exam
    template_name='home.html'

def delete_exam(request, pk):
    obj_list = Exam.objects.filter(id=pk).first()
    obj_list.delete()
    messages.warning(request, f'Exam "<strong>{obj_list.title}</strong>" delete successfully')
    return redirect('exams:exam_list_view')
