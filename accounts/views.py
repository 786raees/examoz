from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm, UpdateUserForm

@login_required
def HomeView(request):
    return render(request, 'home.html')


def edit_profile_view(request):
    user = request.user
    user_form = UpdateUserForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, request.FILES, instance=user.profile)
    if all((user_form.is_valid(), profile_form.is_valid())):
        user_form.save()
        profile_form.save()
        messages.success(request, 'Profile successfully edited')
        return redirect('accounts:edit_profile_view')
    if any((user_form.errors,profile_form.errors)):
        messages.warning(request, 'Please fix the following error')
        
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }

    return render(request, 'account/profile.html', context)
