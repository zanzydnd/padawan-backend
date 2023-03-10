# Generated by Django 4.1.4 on 2023-03-10 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0006_algscenario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='algscenario',
            options={'verbose_name': 'Сценарий(Алгоритмы)', 'verbose_name_plural': 'Сценарии(Алгоритмы)'},
        ),
        migrations.CreateModel(
            name='AlgScenarioStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
                ('input', models.TextField(verbose_name='Подается на вход')),
                ('expected', models.TextField(verbose_name='Ожидаемый результат')),
                ('scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='testing.algscenario', verbose_name='Сценарий')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
    ]