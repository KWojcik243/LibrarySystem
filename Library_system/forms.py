from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Author


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "First name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Last name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Password"}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class BookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Book name"}))
    age_group = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Age group"}))
    rating = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Rating", 'max': '10'}))
    isbn = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "ISBN"}))
    category = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Category"}))

    class Meta:
        model = Book
        fields = ['name', 'age_group', 'rating', 'isbn', 'category']


class AuthorForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "First name"}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Last name"}))

    class Meta:
        model = Author
        fields = ['name', 'surname']
