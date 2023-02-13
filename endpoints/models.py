from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Esp(models.Model):
    status = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )


@receiver(post_save, sender=Esp)
def handle_post_save(sender, instance, **kwargs):
    # get the channel layer
    channel_layer = get_channel_layer()

    # construct the channel name
    channel_name = 'esp_%s' % instance.token

    # construct the message payload
    payload = {
        "type": "my.message",
        "data": {
            "id": instance.id,
            # add any other fields that you want to include in the message
        },
    }

    # send the message to the channel
    async_to_sync(channel_layer.group_send)(channel_name, payload)
