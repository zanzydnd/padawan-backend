# Generated by Django 4.1.4 on 2023-03-02 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(max_length=255, verbose_name='Описание')),
                ('assigment_type', models.CharField(choices=[('AL', 'Алгоритмическое'), ('API', 'Проверка API')], default='API', max_length=255)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('due_to', models.DateTimeField(auto_now=True)),
                ('one_try', models.BooleanField(default=False)),
                ('max_points', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Scenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('max_points', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StaticCodeAnalysisBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaticCodeAnalysisPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_points', models.PositiveIntegerField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.assignment')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.staticcodeanalysisblock')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='static_analysis_blocks',
            field=models.ManyToManyField(related_name='assignments', through='assignment.StaticCodeAnalysisPoint', to='assignment.staticcodeanalysisblock'),
        ),
    ]