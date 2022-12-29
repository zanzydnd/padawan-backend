from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class Classroom(models.Model):
    teacher = models.ForeignKey(USER_MODEL, on_delete=models.SET_NULL, verbose_name="classrooms")

    name = models.CharField(255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    unique_code = models.CharField(255, unique=True, verbose_name="Уникальный код",
                                   help_text="Генерируется Автоматически")

    created_at = models.DateTimeField(auto_now=True)

    students = models.ManyToManyField(USER_MODEL, verbose_name="classrooms")

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        db_table = "classroom"
