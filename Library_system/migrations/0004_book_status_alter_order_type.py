# Generated by Django 4.0.6 on 2022-07-30 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library_system', '0003_author_book_order_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.IntegerField(),
        ),
    ]