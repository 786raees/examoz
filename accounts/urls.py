from django.urls import path
from . import views as account_views

app_name = "accounts"

urlpatterns = [
    path("login/", account_views.login_view, name="login_view")
]
