from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .models import User


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'surname', 'email', 'password']

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Last name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
