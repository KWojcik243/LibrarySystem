from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib import messages


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
    print('a')
    if request.user.is_authenticated:
        return redirect('home')
    print('b')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(user)
            login(request, user)
            redirect('')
        return render(request, 'login.html')
    else:
        print('c')
        return render(request, 'login.html')


def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
