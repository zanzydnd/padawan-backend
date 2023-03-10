from django.db import models

from padawan.models import Orderable


class ScenarioConfig(models.Model):
    timeout = models.PositiveIntegerField(default=10, verbose_name="Таймаут от зароса")

    class Meta:
        verbose_name = "Конфиг Сценария(Api задание)"
        verbose_name_plural = "Конфииги Сценариев(Api задание)"


class Scenario(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    max_points = models.PositiveIntegerField()

    config = models.OneToOneField(ScenarioConfig, on_delete=models.SET_NULL, null=True, verbose_name="Конфиг",
                                  related_name="scenario", blank=True)

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
    class ValidatorType(models.TextChoices):
        STATUS = "Валидатор статуса", "expected_status"
        COMPARATOR = "Сравниватель", "comparator"

    type = models.CharField(choices=ValidatorType.choices, default=ValidatorType.STATUS, max_length=200)

    points = models.PositiveIntegerField(default=0, help_text="Кол-во баллов за успех")
    actual = models.TextField(null=True, blank=True)
    expected = models.TextField()

    step = models.ForeignKey(Step, related_name="validators", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Валидатор шага"
        verbose_name_plural = "Валидаторы шага"


class AlgScenario(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название сценария")
    max_points = models.PositiveIntegerField()

    def __str__(self):
        return f"Алгоритм: {self.name}"
