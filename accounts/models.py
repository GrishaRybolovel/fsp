from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models

from DjangoAPIFlutter.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    ROLE_CHOICES = [
        ('FM', 'Фермер'),
        ('BY', 'Покупатель'),
        ('AD', 'Админ')
    ]
    role = models.CharField(max_length=3,
                               choices=ROLE_CHOICES,
                               default='SL',
                               verbose_name='Роль',
                               blank=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null = True, blank=True)
    card = models.CharField(max_length=20, null=True, blank=True)
    chats = models.ManyToManyField(
        "Chat",
        related_name='chats',
        blank=True,
        verbose_name='Чаты'
    )


    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Item(models.Model):
    name = models.CharField(max_length=63, verbose_name='Название')
    cost_retail = models.FloatField(verbose_name='Розничная цена')
    cost_wholesale = models.FloatField(blank=True, null=True, verbose_name='Оптовая цена')
    doc = models.FileField(upload_to='uploads/', verbose_name='Фото')
    date = models.DateField(verbose_name='Дата готовности', blank=True, null=True)
    farmer = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Владелец')
    number = models.FloatField(verbose_name='Количество товара')
    number_wholesale = models.FloatField(blank=True, null=True, verbose_name='Мин. кол-во товара для оптовой закупки')
    description = models.CharField(max_length=63, verbose_name='Описание')
    expire_date = models.DateField(verbose_name='Дата окончания срока годности', blank=True, null=True)
    number_for_month = models.FloatField(blank=True, null=True, verbose_name='Количество товара на месяц(подписка)')
    subscriptable = models.BooleanField(verbose_name="Возможность подписки")
    ITEM_CHOICES = [
        ('FR', 'Фрукты'),
        ('VE', 'Овощи'),
        ('OT', 'Другие')
    ]
    category = models.CharField(max_length=2,
                               choices=ITEM_CHOICES,
                               default='OT',
                               verbose_name='Категории',
                                )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель', null=True)
    text = models.CharField(max_length=2048, blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'

class Chat(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name='Название чата')
    messages = models.ManyToManyField(
        "Message",
        related_name="messages",
        blank=True,
        verbose_name='Сообщения'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'