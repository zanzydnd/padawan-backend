from admin_interface.models import Theme
from django.db import models

# Create your models here.

class ThemeProxy(Theme):
    class Meta:
        proxy = True
        verbose_name = "Тема"
        verbose_name_plural = "Темы"