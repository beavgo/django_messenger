from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core import views


urlpatterns = [
    path('', views.chats_list, name='chats'),
    path('admin/', admin.site.urls),
    path('profile/create/', views.create_profile),
    path('profile/<str:username>', views.get_profile),
    path('<slug:url>/', views.get_chat, name='chat-detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)