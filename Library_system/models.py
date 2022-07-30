from django.db import models
from django.contrib.auth.models import User

# class User(models.Model):
#     # id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=40)
#     surname = models.CharField(max_length=40)
#     email = models.EmailField()
#     password = models.CharField(max_length=50)
#     access_type = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name + ' ' + self.surname


class Author(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)

    def __str__(self):
        return (self.name, self.surname, self.id)


class Book(models.Model):
    name = models.CharField(max_length=400)
    age_group = models.IntegerField()
    rating = models.IntegerField()
    isbn = models.IntegerField()
    category = models.CharField(max_length=50)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)


class Order(models.Model):
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE)
    action_start_time = models.DateTimeField()
    action_end_time = models.DateTimeField()
    type = models.BooleanField()  # True == borrowed, False == reservation
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
