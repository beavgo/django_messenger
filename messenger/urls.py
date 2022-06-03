from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.chats_list, name='chats'),
    path('admin/', admin.site.urls),
]
