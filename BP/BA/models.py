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
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='Биография')

    def clean(self):
        super().clean()
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.last_name):
            raise ValidationError('Фамилия должна содержать только кириллические буквы, пробелы и дефисы.')
        if not re.match(r'^[А-Яа-яЁёs-]*$', self.first_name):
            raise ValidationError('Имя должно содержать только кириллические буквы, пробелы и дефисы.')
        if self.middle_name and not re.match(r'^[А-Яа-яЁёs-]*$', self.middle_name):
            raise ValidationError('Отчество должно содержать только кириллические буквы, пробелы и дефисы.')



from django.contrib.auth import get_user_model
User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'