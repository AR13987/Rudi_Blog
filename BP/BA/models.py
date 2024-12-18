from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
import re
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=False, verbose_name='Фамилия')
    username = models.CharField(max_length=150, unique=True, blank=False, verbose_name='Логин')
    email = models.EmailField(unique=True, blank=False, verbose_name='Электронная почта')
    middle_name = models.CharField(max_length=150, blank=False, verbose_name='Отчество')
    password1 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Пароль')
    password2 = models.CharField(max_length=128, blank=False, null=True, verbose_name='Повтор пароля')
    consent = models.BooleanField(default=False, verbose_name='Я соглашаюсь на обработку моих персональных данных')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='groups_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def clean(self):
        super().clean()
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.last_name):
            raise ValidationError('Фамилия должна содержать только кириллические буквы, пробелы и дефисы.')
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.first_name):
            raise ValidationError('Имя должно содержать только кириллические буквы, пробелы и дефисы.')
        if self.middle_name and not re.match(r'^[А-Яа-яЁёs-]*$', self.middle_name):
            raise ValidationError('Отчество должно содержать только кириллические буквы, пробелы и дефисы.')
        if not self.consent:
            raise ValidationError('Необходимо согласие на обработку персональных данных.')
