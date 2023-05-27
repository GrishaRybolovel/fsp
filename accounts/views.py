from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet
from django.core import serializers
import imghdr
from mimetypes import guess_extension, guess_type
import base64
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenViewBase


from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import *


class MyIdSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.user.id
        return Response(
            data={
                'id': id
            },
            status=200
        )


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


class PostMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        request.data._mutable = True
        request.data.update({'sender': request.user.id})
        chat = Chat.objects.get(id=chat_id)
        serializer = MessageSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        chat.messages.add(message)
        return Response(
            status=201
        )


class ChatsView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
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
        res = ItemSerializer2(items,
                             context=serializer_context,
                             many=True)
        return Response(
            data = {
                'items' : res.data,
            },
            status=201
        )

    def post(self, request):
        request.data._mutable = True
        tokens = request.data['doc'].split(' ')
        encoded = tokens[0]
        file = ContentFile(base64.b64decode(encoded), name=tokens[1])
        request.data['doc'] = file
        serializer = ItemSerializer1(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        return Response(
            data={
                'Status': 'OK',
                'Name' : item.name
            },
            status=201
        )


class GetChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        request_user = request.user
        commonChats1 = user.chats.filter(user1=request_user.id)
        commonChats2 = user.chats.filter(user2=request_user.id)

        if commonChats1.count() == 0 and commonChats2.count() == 0:
            new_chat = Chat.objects.create_chat(user, request_user, request_user.name, user.name)
            user.chats.add(new_chat)
            request_user.chats.add(new_chat)
            return MessagesView.get(MessagesView, request=request, chat_id=new_chat.id)
        elif commonChats1.count() == 1:
            return MessagesView.get(MessagesView, request=request, chat_id=commonChats1.first().id)
        else:
            return MessagesView.get(MessagesView, request=request, chat_id=commonChats2.first().id)


class MyTokenObtainPairView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(
            data={'info': serializer.data},
            status=201
        )

    def put(self, request):
        request.data._mutable = True
        request.data['email'] = request.user.email
        request.data['name'] = request.user.name
        serializer = UserInfoSerializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)

