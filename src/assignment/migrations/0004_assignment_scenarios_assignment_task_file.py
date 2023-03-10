# Generated by Django 4.1.4 on 2023-03-10 17:44

from django.db import migrations, models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_alter_scenario_options_alter_scenarioconfig_options_and_more'),
        ('assignment', '0003_delete_scenario'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='scenarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='assigments', to='testing.scenario', verbose_name='Сценарии'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='task_file',
            field=models.FileField(blank=True, null=True, upload_to='tasks', verbose_name='Файл с Заданием'),
        ),
    ]
