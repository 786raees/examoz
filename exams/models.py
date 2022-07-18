from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from ckeditor.fields import RichTextField
import uuid

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse('exams:course_add_view')

    def get_edit_url(self):
        return reverse('exams:course_update_view', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('exams:course_delete_view', kwargs={'pk': self.pk})

class Exam(models.Model):

    uid = models.UUIDField(unique=True, default=uuid.uuid4)

    title = models.CharField(_("title"), max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    introduction = RichTextField(null=True, blank=True, help_text="<br>This text is displayed on the top of the test.")
    randomize_question = models.BooleanField( _('Randomize the order of the question'), default=False)
    conclusion_text = RichTextField(null=True, blank=True, help_text="<br>This text is displayed after the test is submited.")
    show_custom_message = models.BooleanField(_("Show custom message if student passed or failed"), default=False)
    passing_score = models.PositiveSmallIntegerField(_("What is the passing score"),null=True)
    pass_message = RichTextField(null=True, blank=True, help_text="<br>If the student passes this message is displayed.")
    fail_message = RichTextField(null=True, blank=True, help_text="<br>If the student fails this message is displayed.")
    # At the end of the test. Display the user's:
    display_score = models.BooleanField(_("Score"), default=False)
    display_test_outline = models.BooleanField(_("test outline"), default=False)
    display_indicate = models.BooleanField(_("Indicate if the answer is correct or not"), default=False)
    display_correct_answer = models.BooleanField(_("Display correct answer"), default=False)
    display_explanation = models.BooleanField(_("explanation"), default=False)

    # who can take your exam
    anyone = models.BooleanField(_("Anyone"), default=False)
    anyone_with_password = models.BooleanField(_("Anyone who enter a password of your choice"), default=False)
    anyone_with_unique_identifier = models.BooleanField(_("Anyone who enter a unique identifier from a list that I specify"), default=False)
    anyone_with_unique_email = models.BooleanField(_("Anyone who enter an E-mail address from a list that I specify"), default=False)
    student_identifier = models.TextField(_("student_identifier"), help_text='What should test takers enter to identify themselves?', default='please enter your school email address')

    # notifications
    class NotificationChoices(models.TextChoices):
        yes = 'yes', 'yes'
        no = 'no', 'no'
    
    notifications = models.CharField(max_length=3, choices=NotificationChoices.choices, default=NotificationChoices.no, help_text='Do you want to receive an email whenever someone finishes this exam?')
    status = models.CharField(_("status"), max_length=50,null=True)
    question = models.CharField(_("question"), max_length=50,null=True)
    no_of_score = models.CharField(_("no of score"), max_length=50,null=True)
    avg_score = models.CharField(_("avg score"), max_length=50,null=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_publish = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("exams:exam_detail_view", kwargs={"pk": self.pk})


class Question(models.Model):
    class QUESTIONTYPE(models.TextChoices):
        multiple_choices_one = 'Multiple Choices (choose one)','Multiple Choices (choose one)'
        multiple_choices_many = 'Multiple Choices (choose many)','Multiple Choices (choose many)'
        true_false = 'True/False','True/False'
        matching = 'Matching','Matching'
        fill_in_the_blank = 'Fill in the blank','Fill in the blank'
        short = 'Short Question','Short Question'
        essay = 'Essay','Essay'
        text_block = 'Text Block','Text Block'
        poll = 'Poll','Poll'
        group = 'Group','Group'

    question_type = models.CharField(choices=QUESTIONTYPE.choices, blank=True, null=True, max_length=30)
    exam_name = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_daata')
    question_title = models.TextField()
    question_marks = models.PositiveIntegerField()
    question_explanation = models.BooleanField(default=False)
    question_explanation_text = models.TextField()

    def __str__(self):
        return str(self.question_title)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return str(self.answer)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.TextField()

    def __str__(self):
        return str(self.option)


class Result(models.Model):
    email = models.EmailField(max_length=254)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)
    partial_question = models.ManyToManyField(Question, related_name='partial_question')

    def __str__(self):
        return str(self.email)