from django.urls import path
from . import views as exam_view

app_name = "exams"

urlpatterns = [
    path("", exam_view.ExamList.as_view(), name="exam_list_view"),
    path("<uuid:uid>/", exam_view.take_student_identity, name="take_student_identity"),
    path("exam/add/", exam_view.ExamCreateView.as_view(), name="exam_add_view"),
    path("exam/<int:pk>/", exam_view.ExamDetailView.as_view(), name="exam_detail_view"),
    path("exam/change/<int:pk>/", exam_view.ExamUpdateView.as_view(), name="exam_update_view"),
    path("exam/delete/<int:pk>/", exam_view.delete_exam, name="exam_delete_view"),
    path("exam/setting/change/<int:pk>/", exam_view.ExamSettingUpdateView.as_view(), name="exam_setting_update_view"),
    path("exam/question/add/<int:pk>/", exam_view.question_add_page, name="question_add_view"),
    path("exam/publish/<int:uid>/", exam_view.publish_page, name="publish_page"),
    path("exam/result/<int:pk>/", exam_view.result_page, name="result_page"),
    path("exam/exam_form_handler/", exam_view.exam_form_handler, name="exam_form_handler"),
    path("course/add/", exam_view.CourseCreateView.as_view(), name="course_add_view"),
    path("course/change/<int:pk>/", exam_view.CourseUpdateView.as_view(), name="course_update_view"),


]
