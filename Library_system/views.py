from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm, BookForm, AuthorForm
from .models import Book, Author, Order
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta


@login_required(login_url='login')
def home(request):
    all_books = Book.objects.all
    return render(request, 'home.html', {'all': all_books})


@login_required(login_url='login')
def reservation(request):
    all_books = Book.objects.all
    all_orders = Order.objects.all
    if request.method == "POST":
        book = request.POST.get('reservation')
        book = Book.objects.get(id=book)
        order = Order()
        order.book_id_id = book.id
        order.action_start_time = datetime.now()
        order.action_end_time = datetime.now() + timedelta(days=1)
        order.type = 2
        book.status = 2
        book.save()
        # actual_logged_user = User.objects.get(id=request.user.id)
        # order.user_id = User.objects.get(id=actual_logged_user.id)
        order.user_id = User.objects.get(id=request.user.id)
        order.save()
    return render(request, 'home.html', {'all': all_books, 'orders': all_orders})


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
    all_books = Book.objects.all
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            author = request.POST.get('author')
            book = form.save(commit=False)
            book.author_id = Author.objects.get(id=author)
            book.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'add_book.html', {'form': form, 'authors': all_authors, 'book': all_books})


@login_required(login_url='login')
def delete_book(request):
    form = BookForm()
    all_authors = Author.objects.all
    all_books = Book.objects.all
    if request.method == "POST":
        book = request.POST.get('delete')
        Book.objects.filter(id=book).delete()
    return render(request, 'add_book.html', {'form': form, 'authors': all_authors, 'book': all_books})


@login_required(login_url='login')
def add_author(request):
    form = AuthorForm()
    all_authors = Author.objects.all
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'add_author.html', {'form': form, 'authors': all_authors})


@login_required(login_url='login')
def delete_author(request):
    form = AuthorForm()
    all_authors = Author.objects.all
    if request.method == "POST":
        author = request.POST.get('delete')
        Author.objects.filter(id=author).delete()
    return render(request, 'add_author.html', {'form': form, 'authors': all_authors})


def logout_user(request):
    logout(request)
    return redirect('login')
