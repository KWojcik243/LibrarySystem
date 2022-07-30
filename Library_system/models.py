from django.db import models
from django.contrib.auth.models import User


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
    status = models.IntegerField(default=0, editable=False)


class Order(models.Model):
    book_id = models.OneToOneField(Book, on_delete=models.CASCADE)
    action_start_time = models.DateTimeField()
    action_end_time = models.DateTimeField()
    type = models.IntegerField()  # 0 == available, 1 == borrowed, 2 == reserved
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
