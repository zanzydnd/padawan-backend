from django.contrib.auth import get_user_model
from django.db import models
from sortedm2m.fields import SortedManyToManyField

from classroom.models import Classroom
from testing.models import Scenario, AlgScenario, Step, AlgScenarioStep, StepValidator

User = get_user_model()


class Assignment(models.Model):
    class Type(models.TextChoices):
        algorithm = "AL", "Алгоритмическое"
        api = "API", "Проверка API"

    classroom = models.ForeignKey(Classroom, related_name="assignments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=255, verbose_name="Описание")
    assigment_type = models.CharField(max_length=255, choices=Type.choices, default=Type.api)

    created_at = models.DateTimeField(auto_now=True, editable=False)
    due_to = models.DateTimeField(auto_now=True, editable=True)

    one_try = models.BooleanField(default=False)

    max_points = models.PositiveIntegerField()

    static_analysis_blocks = models.ManyToManyField(to="assignment.StaticCodeAnalysisBlock", related_name="assignments",
                                                    verbose_name="Блоки статического анализа", blank=True)
    # submissions = models.ManyToManyField(to=User, through="AssignmentSubmission", )

    task_file = models.FileField(verbose_name="Файл с Заданием", upload_to="tasks", null=True, blank=True)

    api_scenarios = SortedManyToManyField(Scenario, related_name="assigments", verbose_name="Сценарии", blank=True)
    alg_scenarios = SortedManyToManyField(AlgScenario, related_name="assigments", verbose_name="Сценарии", blank=True)

    def __str__(self):
        return self.name


class AssignmentSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    status = models.CharField(max_length=25, default="В процессе")
    date = models.DateField(auto_now_add=True)  # дата поступления

    git_url = models.URLField(null=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.name}"


class AlgSubmissionResults(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.SET_NULL, null=True)
    step = models.ForeignKey(AlgScenarioStep, on_delete=models.CASCADE, verbose_name="submission_results")
    success = models.BooleanField(default=True)
    time = models.DurationField(null=True)
    actual = models.TextField(null=True)


class ApiSubmissionResults(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.SET_NULL, null=True, related_name="results")
    validator = models.ForeignKey(StepValidator, on_delete=models.CASCADE, null=True,
                                  related_name="validated_submissions")
    success = models.BooleanField(default=True)
    headers = models.JSONField(null=True)
    body = models.JSONField(null=True)
    message = models.TextField(null=True)
    status = models.TextField(null=True)


class StaticCodeAnalysisBlock(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Блок Статического анализа"
        verbose_name_plural = "Блоки Статического анализа"


class StaticSubmissionResults(models.Model):
    submission = models.ForeignKey(AssignmentSubmission, on_delete=models.SET_NULL, null=True)
    block = models.ForeignKey(StaticCodeAnalysisBlock, on_delete=models.CASCADE)
    result = models.TextField()
