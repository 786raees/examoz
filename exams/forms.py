from django import forms
from .models import Exam, Question

class ExamSettingsForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        exclude = ('uid','status','question','no_of_score','avg_score',)
        

class QuestionInsert(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_title','question_type','question_marks','question_explanation','question_explanation_text')
        widgets = {
            'question_title': forms.Textarea(attrs={'rows':3})
        }
        