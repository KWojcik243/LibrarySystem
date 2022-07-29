# Generated by Django 4.0.6 on 2022-07-29 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Library_system', '0002_alter_user_access_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('surname', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('age_group', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('isbn', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Library_system.author')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_start_time', models.DateTimeField()),
                ('action_end_time', models.DateTimeField()),
                ('type', models.BooleanField()),
                ('book_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Library_system.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
