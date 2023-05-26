from django.contrib import admin
from .models import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'farmer')
    list_display_links = ('id',)
    search_fields = ('id', 'name',)

admin.site.register(Item, ItemAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'full_name', 'address', 'phone_number', 'card')
    list_display_links = ('id',)
    search_fields = ('id', 'username', 'full_name')

admin.site.register(User, UserAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'text', 'created_at')
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Message, MessageAdmin)

class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_display_links = ('id',)
    search_fields = ('id',)

admin.site.register(Chat, ChatAdmin)