from rest_framework import serializers

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', "email", 'first_name', "last_name", 'password', 'profile', ]

        read_only_fields = ['email', 'profile']

class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    is_active = serializers.HiddenField(default=0)
    #recaptcha = ReCaptchaV2Field()

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            return email

        raise serializers.ValidationError("Email is already exists")