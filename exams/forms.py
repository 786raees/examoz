from django import forms
from .models import Exam, Question

class ExamSettingsForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        exclude = ('status','question','no_of_score','avg_score',)
        

class QuestionInsert(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_type',)
        