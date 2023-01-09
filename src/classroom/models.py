import uuid

from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class Classroom(models.Model):
    teacher = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, verbose_name="Учитель",
                                related_name="head_in_classrooms")

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    unique_code = models.CharField(max_length=255, unique=True, default=uuid.uuid4().hex[:5].upper(),
                                   verbose_name="Уникальный код",
                                   help_text="Генерируется Автоматически")

    created_at = models.DateTimeField(auto_now=True)

    students = models.ManyToManyField(USER_MODEL, verbose_name="Ученики", related_name="participated_classrooms")

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        db_table = "classroom"
