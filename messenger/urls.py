from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from core import views
from django.contrib.auth import views as authViews


urlpatterns = [
    path('', views.chats_list, name='chats'),
    path('admin/', admin.site.urls),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', authViews.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/create/', views.create_profile),
    path('profile/<str:username>', views.get_profile),
    path('<slug:url>/', views.get_chat, name='chat-detail'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)