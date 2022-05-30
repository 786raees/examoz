from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, User

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)