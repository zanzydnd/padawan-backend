# Generated by Django 4.1.4 on 2023-03-09 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0008_alter_classroom_unique_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='unique_code',
            field=models.CharField(help_text='Генерируется Автоматически', max_length=255, unique=True, verbose_name='Уникальный код'),
        ),
    ]
