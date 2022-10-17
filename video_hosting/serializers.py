import djoser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from drf_recaptcha.fields import ReCaptchaV2Field
from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import Video, Channel, Profile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
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


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    #recaptcha = ReCaptchaV2Field()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            return email

        raise serializers.ValidationError("Email is already exists")

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        return user

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': False},
                        'last_name': {'required': False}}
