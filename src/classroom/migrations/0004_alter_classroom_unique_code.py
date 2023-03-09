# Generated by Django 4.1.4 on 2023-03-04 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_alter_classroom_unique_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='unique_code',
            field=models.CharField(default='64271', help_text='Генерируется Автоматически', max_length=255, unique=True, verbose_name='Уникальный код'),
        ),
    ]
