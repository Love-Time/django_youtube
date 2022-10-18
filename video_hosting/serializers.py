
from django.core.validators import FileExtensionValidator

from rest_framework import serializers


from users.models import CustomUser
from .models import Video, Channel

class CurrentChannelDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.channel








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



    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_active']
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': False},
                        'last_name': {'required': False}}
