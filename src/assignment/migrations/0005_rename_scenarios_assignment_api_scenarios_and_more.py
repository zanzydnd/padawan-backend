# Generated by Django 4.1.4 on 2023-03-10 17:52

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_algscenario'),
        ('assignment', '0004_assignment_scenarios_assignment_task_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='scenarios',
            new_name='api_scenarios',
        ),
        migrations.AddField(
            model_name='assignment',
            name='alg_scenarios',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='assigments', to='testing.algscenario', verbose_name='Сценарии'),
        ),
    ]
