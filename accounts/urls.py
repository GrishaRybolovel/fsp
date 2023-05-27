from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MyTokenObtainPairView

from accounts.views import *

router = DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('info/', InfoView.as_view(), name = 'info'),
    path('getId/', MyIdSet.as_view(), name='myid'),
    path('get_chat/<int:user_id>', GetChatView.as_view(), name='get_chat'),
    path('chat/<int:chat_id>', MessagesView.as_view(), name='chat'),
    path('chat/<int:chat_id>/post_message', PostMessageView.as_view(), name='post_message'),
    path('chats/', ChatsView.as_view(), name='get_chats'),
    path('items/', ItemsView.as_view(), name='get_items'),
    path('farmer/', ItemsView2.as_view(), name='get_items_farmer'),
    path("", include(router.urls))
]
