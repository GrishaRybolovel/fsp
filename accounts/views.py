from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from django.core import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import *


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(
            data=UserSerializer(request.user).data
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            data={
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=201
        )


class ChatsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        chats = []
        for c in request.user.chats.all():
            chats.append(Chat.objects.get(id=c.id))
        res = ChatSerializer(chats, many=True)
        return Response(
            data={
                'chats': res.data,
            }, status=201)

class MessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        chat = Chat.objects.get(id=id)
        messages = chat.messages.all()
        res = MessageSerializer(messages, many=True)
        return Response(
            data={
                'messages': res.data,
            }, status=201)


class ItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()
        serializer_context = {
            'request': request,
        }
        res = ItemSerializer(items,
                             context=serializer_context,
                             many=True)
        return Response(
            data = {
                'items' : res.data,
            },
            status=201
        )

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        return Response(
            data={
                'Status': 'OK',
                'Name' : item.name
            },
            status=201
        )