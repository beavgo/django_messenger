from http.client import HTTPResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from transliterate import translit
from .models import Chat, Message, Profile
from django.contrib.auth.models import User
from .forms import MessageCreateForm, ProfileCreateForm, UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login


@login_required
def chats_list(request):
    # Фильтруем чаты, в которых есть авторизованный пользователь
    chats = Chat.objects.filter(members__in=[request.user.id])

    # Если есть чаты у пользователя, то выводим их, иначе
    # информируем об их отсутствии с помоощью bool-переменной
    if chats.exists():
        return render(request,
                      'dashboard/chats_list.html',
                      {'chats': chats,
                       'boolean': True})
    else:
        return render(request,
                      'dashboard/chats_list.html',
                      {'boolean': False})


@login_required
def get_chat(request, url):
    chat = get_object_or_404(Chat, slug=url)
    messages = Message.objects.filter(chat=chat)

    if request.method == 'POST':
        # Создание и отправка сообщения
        message_form = MessageCreateForm(data=request.POST)

        if message_form.is_valid():
            # Создание сообщения, но без сохранения в БД
            new_message = message_form.save(commit=False)
            new_message.chat = chat
            new_message.sender = request.user
            # Сохранение сообщения в БД
            new_message.save()
    else:
        message_form = MessageCreateForm()
    
    return render(request, 
                  'dashboard/chat_detail.html',
                  {'messages': messages,
                   'title': chat.title,
                   'url': url,
                   'message_form': message_form})


@login_required
def create_profile(request):
    if request.method == 'POST':
        profile_form = ProfileCreateForm(data=request.POST, files=request.FILES)

        if profile_form.is_valid():
            new_profile = profile_form.save(commit=False)
            # Прикрепляем пользователя к профилю
            new_profile.user = request.user
            new_profile.save()
            return redirect("/")
    else:
        profile_form = ProfileCreateForm()
    
    return render(request,
                  'registration/profile_creation.html',
                  {'profile_form': profile_form})


def get_profile(request, username):
    try:
        user = User.objects.get(username=username)
        # Получаем объект профиля, используя имя пользователя
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        return HTTPResponse('Такого пользователя не существует')

    return render(request,
                  'registration/profile_page.html',
                  {'profile': profile,
                   'username': username})


def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # Устанавливаем пароль пользователя
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Перенаправляем на страницу создания профиля
            return redirect('profile/create/')
    else:
        user_form = UserRegistrationForm()
    
    return render(request,
                  'registration/user_registration.html',
                  {'user_form': user_form})


def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            cd = login_form.cleaned_data
            # Получаем объект пользователя
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                # Заходим под полученным пользователем
                login(request, user)
                return redirect("/")
            else:
                return HTTPResponse('Аккаунт деактивирован')
        else:
            return render(request,
                          'registration/login.html',
                          {'login_form': login_form,
                           'invalid_data':'Неверное имя пользователя или пароль'})
    else:
        login_form = LoginForm()
    
    return render(request,
                  'registration/login.html',
                  {'login_form': login_form,
                   'invalid_data':''})
