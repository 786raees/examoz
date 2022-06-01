from django.urls import path
from . import views as exam_view

app_name = "exams"

urlpatterns = [
    path("", exam_view.ExamList.as_view(), name="exam_list_view"),
    path("exam/add/", exam_view.ExamCreateView.as_view(), name="exam_add_view"),
    path("exam/<int:pk>/", exam_view.ExamDetailView.as_view(), name="exam_detail_view"),
    path("exam/change/<int:pk>/", exam_view.ExamUpdateView.as_view(), name="exam_update_view"),
    path("exam/delete/<int:pk>/", exam_view.delete_exam, name="exam_delete_view"),
]
