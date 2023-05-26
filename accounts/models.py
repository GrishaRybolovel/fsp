from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models

from DjangoAPIFlutter.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True,
                                help_text='Обязательно. Не более 150 символов. Можно использовать цифры и буквы',
                                validators=[ASCIIUsernameValidator],
                                error_messages={'unique': "Пользователь с таким именем уже существует"})
    full_name = models.CharField(max_length=150)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null = True, blank=True)
    card = models.CharField(max_length=20, null=True, blank=True)


    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.username)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'