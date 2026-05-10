from django.contrib import admin

from apps.friendships.models import FriendRequest, Friendship


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'status', 'created_at', 'responded_at')
    list_filter = ('status',)
    search_fields = ('sender__username', 'receiver__username')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'receiver', 'created_at')
    search_fields = ('requester__username', 'receiver__username')
