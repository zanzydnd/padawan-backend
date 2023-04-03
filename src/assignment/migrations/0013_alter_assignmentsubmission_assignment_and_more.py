# Generated by Django 4.1.4 on 2023-04-03 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0012_remove_assignment_submissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='assignment.assignment'),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
    ]
