# Generated by Django 4.1.4 on 2023-04-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0008_remove_scenario_config_remove_stepvalidator_actual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='algscenariostep',
            name='time',
            field=models.DurationField(null=True),
        ),
    ]
