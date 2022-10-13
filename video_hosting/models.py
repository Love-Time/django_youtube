from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='image/%Y/%m/%d/')
    file = models.FileField(
        upload_to='video/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', "mvk"])],

    )
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey("Channel", verbose_name="Канал", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class Channel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    image = models.ImageField(upload_to='image/profile/image/%Y/%m/', null=True)
    banner = models.ImageField(upload_to='image/profile/banner/%Y/%m/', null=True)
    logo = models.ImageField(upload_to='image/profile/logo/%Y/%m/', null=True)

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.filter(email=username)[:1][0]
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None