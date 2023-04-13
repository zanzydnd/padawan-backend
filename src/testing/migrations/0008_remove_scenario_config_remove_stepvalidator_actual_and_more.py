# Generated by Django 4.1.4 on 2023-03-26 11:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0007_alter_algscenario_options_algscenariostep'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='config',
        ),
        migrations.RemoveField(
            model_name='stepvalidator',
            name='actual',
        ),
        migrations.RemoveField(
            model_name='stepvalidator',
            name='expected',
        ),
        migrations.RemoveField(
            model_name='stepvalidator',
            name='type',
        ),
        migrations.AddField(
            model_name='stepvalidator',
            name='allowed_response_statuses',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), null=True, size=None, verbose_name='Разрешенные статусы'),
        ),
        migrations.AddField(
            model_name='stepvalidator',
            name='expected_response_body',
            field=models.TextField(null=True, verbose_name='Ожидаемое тело ответа'),
        ),
        migrations.AddField(
            model_name='stepvalidator',
            name='timeout',
            field=models.PositiveIntegerField(default=60, verbose_name='Таймаут'),
        ),
        migrations.AlterField(
            model_name='stepvalidator',
            name='points',
            field=models.PositiveIntegerField(verbose_name='Баллы'),
        ),
        migrations.DeleteModel(
            name='ScenarioConfig',
        ),
    ]