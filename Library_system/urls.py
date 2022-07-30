from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_user, name="logout"),
    path('add_book/', views.add_book, name="add_book"),
    path('add_author/', views.add_author, name="add_author"),
    path('delete_book/', views.delete_book, name="delete_book"),
    path('delete_author/', views.delete_author, name="delete_author"),
    path('reservation/', views.reservation, name="reservation"),
]
