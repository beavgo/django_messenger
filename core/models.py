from distutils.command.upload import upload
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


class Message(models.Model):
    sender = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='sender')
    recipient = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='recipient')
    message_text = models.TextField()
    sent = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['sent']

    def __str__(self):
        return f'From: {self.sender}\nTo: {self.recipient}\nAt: {self.sent}'