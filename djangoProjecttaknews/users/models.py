
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLES = (
        ('admin', 'مدیر'),
        ('author', 'نویسنده'),
        ('user', 'کاربر عادی'),
    )
    username = models.CharField(max_length=50,
                                unique=True,
                                verbose_name='نام کاربری'
                                )
    role = models.CharField(max_length=10, choices=ROLES, default='user', verbose_name='نقش')
    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name='تصویر پروفایل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

    @property
    def is_author(self):
        return self.role == 'author'