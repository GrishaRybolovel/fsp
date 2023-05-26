from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'created_at', 'sender', 'id',]

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user1', 'user2', 'name1', 'name2', 'id']


class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    # username = serializers.CharField()
    # password = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'full_name', 'password', 'email', 'role']
        write_only_fields = ['password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user


