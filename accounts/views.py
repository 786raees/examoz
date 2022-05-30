from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def HomeView(request):
    return render(request, 'base_app.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("____________________________")
        print("username: ",username)
        print("password: ",password)

    return render(request, 'auth/login.html')