from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "status","image"]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})  # 👈 calendar picker
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # Inside UserRegistrationForm, add this field
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
