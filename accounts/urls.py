from django.urls import path
from . import views as account_views

app_name = "accounts"

urlpatterns = [
    path("profile/", account_views.edit_profile_view, name="edit_profile_view"),
    path("change/theme/", account_views.change_theme, name="change_theme")
]
