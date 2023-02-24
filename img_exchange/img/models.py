from django.db import models
from django.contrib.auth import get_user_model
from core.models import CreatedModel
User = get_user_model()


class ImagePost(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Автор поста'
    )
    image_1 = models.ImageField(
        upload_to='images/'
    )
    image_2 = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True
    )
    image_3 = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )


class Like(models.Model):
    image = models.ForeignKey(
        ImagePost,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Автор like'
    )
