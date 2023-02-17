from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

websocket_data = Signal()
# Create your models here.
class Esp(models.Model):
    status = models.BooleanField(default=False)
    token = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, )

    @staticmethod
    def give_esp_statue(token):
        esp = Esp.objects.get(token=token)
        data = {'statue': esp.status}

        return data


@receiver(post_save, sender=Esp)
def handle_post_save(sender, instance, **kwargs):
    if instance.pk is None:
        # new instance, nothing to do
        return
    # get the channel layer

    channel_layer = get_channel_layer()
    # construct the channel name
    channel_name = 'esp_%s' % instance.token
    # construct the message payload
    data = instance.give_esp_statue(token=instance.token)
    data['type'] = 'statue_updated'
    print('sending....')
    # send the message to the channel
    async_to_sync(channel_layer.group_send)(channel_name, data)
