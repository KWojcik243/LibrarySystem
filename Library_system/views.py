from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Concat
from django.db.models import Value
from django.shortcuts import render, redirect
from .forms import CreateUserForm, BookForm, AuthorForm
from .models import Book, Author, Order
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta


# TOODOO order_exec empty push
# Add permisions
@login_required(login_url='login')
def home(request):
    all_books = Book.objects.all
    return render(request, 'home.html', {'all': all_books})


def search(request):
    search = request.POST.get('search')
    queryset = Author.objects.annotate(search_name=Concat('name', Value(' '), 'surname')).filter(search_name__icontains=search).values_list('id', flat=True)
    list=[]
    for dic in queryset.values():
        list.append(int(dic['id']))
    books_by_author = Book.objects.filter(author_id__id__in=list)
    books_by_name = Book.objects.filter(name__icontains=search)
    all_books = books_by_author | books_by_name
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
def my_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id_id=current_user.id)\
        .values('id', 'book_id_id__name', 'action_start_time', 'action_end_time', 'type')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required(login_url='login')
def cancel_reservation(request):
    order_id = request.POST.get('cancel_reservation')
    order = Order.objects.get(id=order_id)
    book = Book.objects.get(id=order.book_id_id)
    book.status = 0
    book.save()
    order.delete()
    return redirect('my_orders')


@login_required(login_url='login')
def man_book(request):
    form = BookForm()
    all_authors = Author.objects.all
    all_books = Book.objects.all
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            author = request.POST.get('author')
            book = form.save(commit=False)
            book.author_id = Author.objects.get(id=author.split(' ')[0])
            book.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'man_book.html', {'form': form, 'authors': all_authors, 'book': all_books})


@login_required(login_url='login')
def delete_book(request):
    form = BookForm()
    all_authors = Author.objects.all
    all_books = Book.objects.all
    if request.method == "POST":
        book = request.POST.get('delete')
        Book.objects.filter(id=book).delete()
    return render(request, 'man_book.html', {'form': form, 'authors': all_authors, 'book': all_books})


@login_required(login_url='login')
def man_author(request):
    form = AuthorForm()
    all_authors = Author.objects.all
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
        else:
            messages.error(request, form.errors)
    return render(request, 'man_author.html', {'form': form, 'authors': all_authors})


@login_required(login_url='login')
def delete_author(request):
    form = AuthorForm()
    all_authors = Author.objects.all
    if request.method == "POST":
        author = request.POST.get('delete')
        Author.objects.filter(id=author).delete()
    return render(request, 'man_author.html', {'form': form, 'authors': all_authors})


@login_required(login_url='login')
def order_exec(request):
    if request.method == 'GET':
        all_user = User.objects.all
        all_order = Order.objects.all
        books_res = Book.objects.filter(status=2).values()
        books_av = Book.objects.filter(status=0).values()
        print(all_user)
        books = books_av | books_res
        # for book in books:
        #     print(book['name'])
        return render(request, 'order_exec.html', {'users': all_user})
    if request.method == 'POST':
        try:
            user = User.objects.get(id=(request.POST.get('user')).split(' ')[0])
        except:
            user = None
        try:
            if int(request.POST.get('res_to_bor')) > 0:
                order = Order.objects.get(id=request.POST.get('res_to_bor'))
                order.type = 1
                order.action_start_time = datetime.now()
                order.action_end_time = datetime.now() + timedelta(days=14)
                book = Book.objects.get(id=order.book_id_id)
                book.status = 1
                book.save()
                order.save()
        except:
            pass
        try:
            if int(request.POST.get('return_book')) > 0:
                order = Order.objects.get(id=request.POST.get('return_book'))
                book = Book.objects.get(id=order.book_id_id)
                book.status = 0
                book.save()
                order.delete()
        except:
            pass

        all_user = User.objects.all
        all_order = Order.objects.filter(user_id_id=user.id)
        # books_res = Book.objects.filter(status=2).values()
        books_av = Book.objects.filter(status=0)
        # print(all_user)
        # books = books_av | books_res
        # for book in books:
        #     print(book['name'])
        return render(request, 'order_exec.html',
                      {'books': books_av, 'users': all_user, 'order': all_order, 'choosen_user': user})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')
