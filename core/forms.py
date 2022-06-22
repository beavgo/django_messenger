from django.forms import ModelForm
from .models import Message, Profile


class MessageCreateForm(ModelForm):
    '''Форма для создания и отправки сообщения
       в чате'''
    class Meta:
        model = Message
        fields = ['message_text']


class ProfileCreateForm(ModelForm):
    '''Форма для создания профиля
       пользователя'''
    class Meta:
        model = Profile
        fields = ['name', 'picture', 'status']
