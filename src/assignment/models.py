from django.db import models


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


class StaticCodeAnalysisPoint(models.Model):
    block = models.ForeignKey("assignment.StaticCodeAnalysisBlock", on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)

    max_points = models.PositiveIntegerField()


class StaticCodeAnalysisBlock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Scenario(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    max_points = models.PositiveIntegerField()
