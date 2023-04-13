from django.contrib.postgres.fields import ArrayField
from django.db import models

from padawan.models import Orderable


class Scenario(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    max_points = models.PositiveIntegerField()

    def __str__(self):
        return f"Api: {self.name}"

    class Meta:
        verbose_name = "Сценарий(Api задание)"
        verbose_name_plural = "Сценарии(Api задание)"


class Step(Orderable):
    class HttpMethodChoices(models.TextChoices):
        GET = "GET", 'GET'
        HEAD = "HEAD", "HEAD"
        POST = "POST", "POST"
        PUT = "PUT", "PUT"
        DELETE = "DELETE", "DELETE"
        PATCH = "PATCH", "PATCH"

    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="steps",
                                 verbose_name="Сценарий")

    url = models.CharField(max_length=255, verbose_name="Относительный путь")
    method = models.CharField(max_length=255, verbose_name="Метод", choices=HttpMethodChoices.choices,
                              default=HttpMethodChoices.GET)

    headers = models.JSONField(verbose_name="Заголовки")
    body = models.TextField(verbose_name="Тело Запроса")

    name = models.CharField(max_length=255, verbose_name="Название шага",
                            help_text="Название шага должно быть уникальным в рамках сценарияд")

    class Meta:
        unique_together = ("scenario", "name")
        ordering = ["order", ]
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"

    def __str__(self):
        return self.name


class StepValidator(models.Model):
    allowed_response_statuses = ArrayField(
        models.PositiveIntegerField(),
        verbose_name="Разрешенные статусы",
        null=True
    )
    expected_response_body = models.TextField(verbose_name="Ожидаемое тело ответа", null=True)
    timeout = models.PositiveIntegerField(verbose_name="Таймаут", default=60)

    points = models.PositiveIntegerField(verbose_name="Баллы")
    step = models.ForeignKey(Step, related_name="validators", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Валидатор шага"
        verbose_name_plural = "Валидаторы шага"


class AlgScenario(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название сценария")
    max_points = models.PositiveIntegerField()

    def __str__(self):
        return f"Алгоритм: {self.name}"

    class Meta:
        verbose_name = "Сценарий(Алгоритмы)"
        verbose_name_plural = "Сценарии(Алгоритмы)"


class AlgScenarioStep(Orderable):
    name = models.CharField(verbose_name="Название", default="Название",max_length=255)
    input = models.TextField(verbose_name="Подается на вход")
    expected = models.TextField(verbose_name="Ожидаемый результат")
    time = models.DurationField(null=True)

    points = models.IntegerField(default=1)

    scenario = models.ForeignKey(AlgScenario, related_name="steps", verbose_name="Сценарий", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
