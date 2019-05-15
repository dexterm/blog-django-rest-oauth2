from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'company', 'fname', 'lname', 'dob')
