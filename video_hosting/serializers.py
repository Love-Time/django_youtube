from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework.response import Response

from .models import Video


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

class VideoSerializer(serializers.ModelSerializer):
    file = serializers.FileField(
                                 validators=[FileExtensionValidator(allowed_extensions=['mp4', "mvk"])],
                                 write_only=True)
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault, read_only=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'image', 'file', 'created_at', 'user']
