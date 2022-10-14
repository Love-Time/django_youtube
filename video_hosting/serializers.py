from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import Video, Channel, Profile


class CurrentChannelDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.channel


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_email', 'is_block']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', "email", 'first_name', "last_name", 'password', 'profile', ]

        read_only_fields = ['email', 'profile']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
        depth = 1


class VideoSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', "mvk"])],
        write_only=True)
    channel = serializers.HiddenField(default=CurrentChannelDefault())
    owner = ChannelSerializer(many=False, source='channel', read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'image', 'file', 'created_at', 'channel', 'owner']
        depth = 1
