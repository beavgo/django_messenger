from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from .forms import MessageForm


@login_required
def chats_list(request):
    chats = Chat.objects.all()
    return render(request, 
                  'dashboard/chats_list.html',
                  {'chats': chats})


@login_required
def chat_page(request, url):
    chat = get_object_or_404(Chat, slug=url)
    messages = Message.objects.filter(chat=chat)

    if request.method == 'POST':
        # Создание и отправка сообщения
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid:
            # Создание сообщения, но без сохранения в БД
            new_message = message_form.save(commit=False)
            new_message.chat = chat
            new_message.sender = request.user
            # Сохранение сообщения в БД
            new_message.save()
    else:
        message_form = MessageForm()
    
    return render(request, 
                  'dashboard/chat_detail.html',
                  {'messages':messages,
                   'title':chat.title,
                   'url': url,
                   'message_form': message_form})
