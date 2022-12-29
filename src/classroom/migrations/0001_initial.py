# Generated by Django 4.1.4 on 2022-12-29 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('unique_code', models.CharField(help_text='Генерируется Автоматически', max_length=255, unique=True, verbose_name='Уникальный код')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('students', models.ManyToManyField(related_name='participated_classrooms', to=settings.AUTH_USER_MODEL, verbose_name='Ученики')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_in_classrooms', to=settings.AUTH_USER_MODEL, verbose_name='Учитель')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
                'db_table': 'classroom',
            },
        ),
    ]
