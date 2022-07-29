from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib import messages


@login_required(login_url='login')
def home(request):
    all_users = User.objects.all
    return render(request, 'home.html', {'all': all_users})


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
        print('i')
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print('j')
            user = form.save(commit=False)
            user.username = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
