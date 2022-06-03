from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat


@login_required
def chats_list(request):
    chats = Chat.objects.all()
    return render(request, 'dashboard/chats_list.html', {'chats': chats})