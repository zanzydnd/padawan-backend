from django.contrib.auth import get_user_model
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from testing.models import Scenario, AlgScenario

User = get_user_model()


class Assignment(models.Model):
    class Type(models.TextChoices):
        algorithm = "AL", "Алгоритмическое"
        api = "API", "Проверка API"

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, verbose_name="Описание")
    assigment_type = models.CharField(max_length=255, choices=Type.choices, default=Type.api)

    created_at = models.DateTimeField(auto_now=True, editable=False)
    due_to = models.DateTimeField(auto_now=True, editable=True)

    one_try = models.BooleanField(default=False)

    max_points = models.PositiveIntegerField()

    static_analysis_blocks = models.ManyToManyField(to="assignment.StaticCodeAnalysisBlock",
                                                    through="assignment.StaticCodeAnalysisPoint",
                                                    related_name="assignments")
    submissions = models.ManyToManyField(to=User, through="AssignmentSubmission", )

    task_file = models.FileField(verbose_name="Файл с Заданием", upload_to="tasks", null=True, blank=True)

    api_scenarios = SortedManyToManyField(Scenario, related_name="assigments", verbose_name="Сценарии",blank=True)
    alg_scenarios = SortedManyToManyField(AlgScenario, related_name="assigments", verbose_name="Сценарии",blank=True)


class AssignmentSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    date = models.DateField(auto_created=True)  # дата поступления


class StaticCodeAnalysisPoint(models.Model):
    block = models.ForeignKey("assignment.StaticCodeAnalysisBlock", on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    max_points = models.PositiveIntegerField()


class StaticCodeAnalysisBlock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
