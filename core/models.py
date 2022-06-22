from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    '''Модель представления профиля пользователя.
       Объект модели профиля связан с объектом модели
       пользователя связью типа Один-к-Одному.'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=350)
    picture = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Chat(models.Model):
    '''Модель представления чата, имеет два варианта реализации:
       диалог - для общения двух пользователей, и группа, где 
       количество пользователей больше двух'''
    DIALOG = 'D'
    GROUP = 'G'
    CHAT_TYPES_CHOICES = (
        (DIALOG, 'Dialog'),
        (GROUP, 'Group'),
    )
    title = models.CharField(max_length=250)
    kind = models.CharField(max_length=1,
                            choices=CHAT_TYPES_CHOICES,
                            default=DIALOG)
    members = models.ManyToManyField(User, related_name='member')
    slug = models.SlugField(max_length=100)

    def get_absolute_url(self):
        return reverse('chat-detail', kwargs={'url':self.slug})
    
    def __str__(self):
        return f'{self.title}'


class Message(models.Model):
    '''Модель представления сообщения. Каждое сообщение связано
       только с одним чатом и одним пользователем'''
    chat = models.ForeignKey(Chat,
                             on_delete=models.CASCADE,
                             related_name='chat')
    sender = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='sender')
    message_text = models.TextField()
    sent = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['sent']

    def __str__(self):
        return f'From: {self.sender}\nAt: {self.sent}\nIn: {self.chat}'
