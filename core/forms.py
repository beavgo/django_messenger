from django.forms import ModelForm
from .models import Message


class MessageForm(ModelForm):
    '''Форма для создания и отправки сообщения
       в чате'''
    class Meta:
        model = Message
        fields = ['message_text']