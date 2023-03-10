from admin_interface.models import Theme
from django.contrib.auth.models import Group
from django.db import models

# Create your models here.

class ThemeProxy(Theme):
    class Meta:
        proxy = True
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

class ProxyGroup(Group):
    class Meta:
        proxy = True