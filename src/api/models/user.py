from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class PadawanUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    class UserStatus(models.TextChoices):
        TEACHER = "Учитель"
        PADAWAN = "Ученик"

    username = None  # отключаем username пользователю.
    status = models.CharField(max_length=255, choices=UserStatus.choices, default=UserStatus.PADAWAN)
    email = models.EmailField(
        verbose_name='Почтовый Адрес',
        max_length=255,
        unique=True,
    )

    def is_teacher(self):
        return self.status == self.UserStatus.TEACHER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "padawan_user"


class ContactService(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=True)
    image = models.ImageField(upload_to="contact_services", verbose_name="Картинка для фронт-енда")

    class Meta:
        verbose_name = "Сервис связи"
        verbose_name_plural = "Сервисы связи"
        db_table = "contact_services"


class PadawanUserContactChoices(models.Model):
    class ChoiceType(models.TextChoices):
        PRIMARY = "Первостепенный"
        SECONDARY = "Второстепенный"

    user = models.ForeignKey(PadawanUser, on_delete=models.CASCADE, related_name="possible_contacts")
    contact_service = models.ForeignKey(ContactService, on_delete=models.CASCADE, related_name="users_choice")

    type = models.CharField(max_length=255, choices=ChoiceType.choices, default=ChoiceType.SECONDARY,
                            verbose_name="Тип")
    value = models.CharField(max_length=255, verbose_name="Значение")

    class Meta:
        verbose_name = "Контакт пользователя"
        verbose_name_plural = "Контакты пользователей"
        db_table = "user_contact"
