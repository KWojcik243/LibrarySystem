from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm, BookForm, AuthorForm
from .models import Book, Author
from django.contrib.auth.models import User
from django.contrib import messages


@login_required(login_url='login')
def home(request):
    # all_books = Book.objects.all
    all_books = Author.objects.all
    return render(request, 'home.html', {'all': all_books})


# def join(request):
#     if request.method == "POST":
#         form = UserForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#         messages.success(request, ('Your Form Has Been Submitted'))
#         return render(request, 'home.html', {})
#     else:
#         return render(request, 'register.html', {})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email__exact=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
def add_book(request):
    form = BookForm()
    all_authors = Author.objects.all
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            author = request.POST.get('author')
            book = form.save(commit=False)
            book.author_id = Author.objects.get(id=author)
            book.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'add_book.html', {'form': form, 'authors': all_authors})


@login_required(login_url='login')
def add_author(request):
    form = AuthorForm()
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'add_author.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
