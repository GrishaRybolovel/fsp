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
    email = models.CharField(max_length=20, null=True, blank=True)
    chats = models.ManyToManyField(
        "Chat",
        related_name='chats',
        blank=True,
        verbose_name='Чаты'
    )


    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'role']

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.username)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Item(models.Model):
    name = models.CharField(max_length=63, blank=True, verbose_name='Название')
    cost_retail = models.IntegerField(blank=True, null=True, verbose_name='Розничная цена')
    cost_wholesale = models.IntegerField(blank=True, null=True, verbose_name='Оптовая цена')
    doc = models.FileField(upload_to='uploads/', verbose_name='Фото')
    date = models.DateField(verbose_name='Дата готовности', blank=True, null=True)
    farmer = models.OneToOneField(User, on_delete=models.deletion.CASCADE, null=True)
    number = models.IntegerField(blank=True, null=True, verbose_name='Количество товара')
    number_wholesale = models.IntegerField(blank=True, null=True, verbose_name='Мин. кол-во товара для оптовой закупки')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель', null=True)
    text = models.CharField(max_length=2048, blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'

class ChatManager(models.Manager):
    def create_chat(self, user1, user2, name1, name2):
        chat = self.create(user1=user1, user2=user2, name1=name1, name2=name2)
        return chat

class Chat(models.Model):
    objects = ChatManager()
    user1 = models.ForeignKey(User, on_delete=models.deletion.CASCADE, verbose_name='Отправитель1', null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.deletion.CASCADE, verbose_name='Отправитель2', null=True, related_name='user2')
    name1 = models.CharField(max_length=255, null=True, verbose_name='Название чата1')
    name2 = models.CharField(max_length=255, null=True, verbose_name='Название чата2')
    messages = models.ManyToManyField(
        "Message",
        related_name="messages",
        blank=True,
        verbose_name='Сообщения'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

