from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class Exam(models.Model):

    title = models.CharField(_("title"), max_length=50)
    status = models.CharField(_("status"), max_length=50)
    question = models.CharField(_("question"), max_length=50)
    no_of_score = models.CharField(_("no of score"), max_length=50)
    avg_score = models.CharField(_("avg score"), max_length=50)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("exams:exam_detail_view", kwargs={"pk": self.pk})
    