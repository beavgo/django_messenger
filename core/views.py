from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message


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

    return render(request, 
                  'dashboard/chat_detail.html',
                  {'messages':messages,
                   'title':chat.title,
                   'url': url})
