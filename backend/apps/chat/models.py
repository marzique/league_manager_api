from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    bumped_at = models.DateTimeField(auto_now_add=True)
    last_message = models.ForeignKey(
        'Message', related_name='last_message_rooms',
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    def increment_version(self):
        self.version += 1
        self.save()
        return self.version

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    room = models.ForeignKey(Room, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rooms', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    # Note, message may have null user – we consider such messages "system". These messages
    # initiated by the backend and have no user author. We are not using such messages in
    # the example currently, but leave the opportunity to extend.
    user = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
