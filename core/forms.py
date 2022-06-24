from django import forms
from .models import Message, Profile
from django.contrib.auth.models import User


class MessageCreateForm(forms.ModelForm):
    '''Форма для создания и отправки сообщения
       в чате'''
    class Meta:
        model = Message
        fields = ['message_text']


class ProfileCreateForm(forms.ModelForm):
    '''Форма для создания профиля
       пользователя'''
    class Meta:
        model = Profile
        fields = ['picture', 'date_of_birth', 'status']


class UserRegistrationForm(forms.ModelForm):
    '''Форма для регистрации пользователей в системе.
       Данная форма предлагает возможность ввода 
       пароля дважды и проверку их соответствия.'''
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    '''Форма для авторизации пользователя'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)