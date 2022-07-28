from django.db import models


class User(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    access_type = models.BooleanField()
    
    def __str__(self):
        return self.name + ' ' + self.surname

