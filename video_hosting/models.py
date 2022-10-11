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
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
