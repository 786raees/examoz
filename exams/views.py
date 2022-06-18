from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Exam, Question, Answer, Option, Result
from .forms import ExamSettingsForm, QuestionInsert
# Create your views here.


class UnSuccessMessageMixin(SuccessMessageMixin):
    """
    Add a unsuccess message on unsuccessful form submission.
    """
    unsuccess_message = ''

    def form_invalid(self, form):
        response = super().form_invalid(form)
        unsuccess_message = self.get_unsuccess_message(form.cleaned_data)
        if unsuccess_message:
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
    fields = ('title',)


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

                print(q, request.POST.get(q))
                if q.startswith('question_type_for_'):
                    type = request.POST.get(q)
                if q.startswith('question_title__question_'):
                    title = request.POST.get(q)

                if q.startswith('question_marks__question_'):
                    marks = request.POST.get(q)
                    question = Question(
                        question_type=type, question_title=title,
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
    exam = Exam.objects.prefetch_related('exam_daata__answer_set','exam_daata__option_set').filter(uid=uid).first()
    context = {'object': exam}

    if not exam.is_publish:
        return render(request, 'exams/exam_not_published.html')

    if request.method == "POST":
        email = request.POST.get("identity")
        context['email'] = email
        return render(request, 'exams/take_exam.html', context)

    return render(request, 'exams/take_student_identity.html', context)


def exam_form_handler(request):

    for q in request.POST:

        if q.startswith('email'):
            email = request.POST.get(q)

        if q.startswith('exam_id'):
            exam_id = request.POST.get(q)
            result = Result(email=email, exam_id=exam_id)
            result.save()


        if q.startswith('option_for_'):
            option = request.POST.get(q).split("_")[-1]
            question_no = str(q).replace('option_for_','')
            answers_list = []

            for q in request.POST:
                if q.startswith(f'answer_for_{question_no}'):
                    answers_list.append(request.POST.get(q))
                    print(q,request.POST.get(q))
            if option in answers_list:
                result.question.add(question_no)
            print(option in answers_list)

    return render(request, 'exams/exam_result.html')


def result_page(request, pk):
    exam = Exam.objects.prefetch_related('exam_daata','result_set__question').filter(pk=pk).first()
    context = {'object': exam}

    return render(request, 'exams/result_page.html', context)