from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.fields import empty, Field
from rest_framework.response import Response

from .models import Video, Channel


# class VideoSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True, label='id')
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField()
#     image = serializers.ImageField()
#     file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp4', "mvk"])])
#     created_at = serializers.DateTimeField(read_only=True)
#
#     def create(self, validated_data):
#         return Video.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.image = validated_data.get('image', instance.image)
#         instance.file = validated_data.get('file', instance.file)
#         instance.save()
#         return instance
class CurrentChannelDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user.channel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"



class VideoSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4', "mvk"])],
        write_only=True)
    channel = serializers.HiddenField(default=CurrentChannelDefault())
    owner = ChannelSerializer(default=CurrentChannelDefault(), source='channel',read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'image', 'file', 'created_at', 'channel', 'owner']



