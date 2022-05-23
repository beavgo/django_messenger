from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='media/avatars/', blank=True)
    status = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Chat(models.Model):
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


class Message(models.Model):
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
