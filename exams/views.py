from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Course, Exam, Question, Answer, Option, Result
from .forms import ExamSettingsForm, QuestionInsert
# Create your views here.


class UnSuccessMessageMixin(SuccessMessageMixin):
    """
    Add a unsuccess message on unsuccessful form submission.
    """
    unsuccess_message = ''

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if unsuccess_message := self.get_unsuccess_message(form.cleaned_data):
            messages.warning(self.request, unsuccess_message)
        else:
            messages.warning(
                self.request, 'Please resolve the following error')
        return response

    def get_unsuccess_message(self, cleaned_data):
        return self.unsuccess_message % cleaned_data


class ExamList(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'home.html'


class ExamCreateView(LoginRequiredMixin, UnSuccessMessageMixin, CreateView):
    model = Exam
    fields = ('title','course')


class ExamUpdateView(LoginRequiredMixin, UnSuccessMessageMixin, UpdateView):
    model = Exam
    # unsuccess_message = 'Exam did not update because of following error'
    success_message = '"<strong>%(title)s</strong>" updated successfully'
    fields = ('title',)


def delete_exam(request, pk):
    obj_list = Exam.objects.filter(id=pk).first()
    obj_list.delete()
    messages.warning(
        request, f'Exam "<strong>{obj_list.title}</strong>" delete successfully')
    return redirect('exams:exam_list_view')

def delete_course(request, pk):
    obj_list = Course.objects.filter(id=pk).first()
    obj_list.delete()
    messages.warning(
        request, f'Course "<strong>{obj_list.name}</strong>" delete successfully')
    return redirect('exams:course_add_view')


class ExamDetailView(DetailView):
    model = Exam


class ExamSettingUpdateView(LoginRequiredMixin, UnSuccessMessageMixin, UpdateView):
    model = Exam
    form_class = ExamSettingsForm
    template_name = 'exams/exam_settings.html'
    success_message = '"<strong>%(title)s</strong>" updated successfully'


def question_add_page(request, pk):
    exam = Exam.objects.filter(pk=pk).first()
    insert_question_form = QuestionInsert()
    if request.method == "POST":


        for q in request.POST:
            if q:

                if q.startswith('question_type_for_'):
                    question_type = request.POST.get(q)

                if q.startswith('question_title__question_'):
                    title = request.POST.get(q)

                if q.startswith('question_marks__question_'):
                    marks = request.POST.get(q)
                    question = Question(
                        question_type=question_type, question_title=title,
                        question_marks=marks, exam_name=exam)
                    question.save()

                if q.startswith('option_value_'):
                    question_option = request.POST.get(q)
                    option = Option(question=question, option=question_option)
                    option.save()

                if q.startswith('answer_for_'):
                    question_answer = request.POST.get(q)
                    answer = Answer(question=question, answer=question_answer)
                    answer.save()

    context = {'insert_question_form': insert_question_form, 'object': exam}
    return render(request, 'exams/question_form.html', context)


def publish_page(request, uid):

    exam = Exam.objects.filter(pk=uid).first()

    if request.method == "POST":
        exam.is_publish = not exam.is_publish
        exam.save()
    context = {'object': exam}
    return render(request, 'exams/publish_page.html', context)


def take_student_identity(request, uid):
    exam = Exam.objects.prefetch_related('exam_daata__answer_set','exam_daata__option_set').filter(uid=uid)
    context = {'object': exam.first()}

    if not exam.first().is_publish:
        return render(request, 'exams/exam_not_published.html')

    if request.method == "POST":

        email = request.POST.get("identity")
        if exam.filter(student_identifier__icontains=email):
            context['email'] = email
            return render(request, 'exams/take_exam.html', context)
        else:
            return HttpResponse('You are not allowed to view this page')

    return render(request, 'exams/take_student_identity.html', context)


def exam_form_handler(request):

    for q in request.POST:

        if q.startswith('email'):
            email = request.POST.get(q)

        if q.startswith('exam_id'):
            exam_id = request.POST.get(q)
            result = Result(email=email, exam_id=exam_id)
            result.save()

        if q.startswith('question_id_'):
            question_id = request.POST.get(q)
            
            answers_set = set()
            options_set = set()

            for items in request.POST:
                if items.startswith(f'option_for_{question_id}'):
                    option = request.POST.get(items)
                    options_set.add(option)

                if items.startswith(f'answer_for_{question_id}'):
                    answer = request.POST.get(items)
                    answers_set.add(answer)

            if options_set == answers_set:
                result.question.add(question_id)

            elif not answers_set.isdisjoint(options_set):
                result.partial_question.add(question_id)

    return render(request, 'exams/exam_result.html')


def result_page(request, pk):
    exam = Exam.objects.prefetch_related('exam_daata','result_set__question').filter(pk=pk).first()
    context = {'object': exam}

    return render(request, 'exams/result_page.html', context)



class CourseCreateView(LoginRequiredMixin, UnSuccessMessageMixin, CreateView):
    model = Course
    fields = ('name',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Course.objects.all()
        return context
    

    


class CourseUpdateView(LoginRequiredMixin, UnSuccessMessageMixin, UpdateView):
    model = Course
    success_message = '"<strong>%(name)s</strong>" updated successfully'
    fields = ('name',)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Course.objects.all()
        return context


def course_delete_view(request, pk):
    obj_list = Course.objects.filter(id=pk).first()
    obj_list.delete()
    messages.warning(
        request, f'Course "<strong>{obj_list.name}</strong>" delete successfully')
    return redirect('exams:course_add_view')