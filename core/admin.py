from django.contrib import admin
from .models import Profile, Message, Chat


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'message_text', 'sent']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'slug']
    prepopulated_fields = {'slug': ('title',)}
