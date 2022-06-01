from django.urls import path
from . import views as exam_view

app_name = "exams"

urlpatterns = [
    path("", exam_view.ExamList.as_view(), name="exam_list_view"),
    path("exam/delete/<int:pk>/", exam_view.delete_exam, name="exam_delete_view"),
]
