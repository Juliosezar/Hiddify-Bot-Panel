import uuid

from django.db import models

class Bots(models.Model):
    name = models.CharField(max_length=50)
    bot_token = models.CharField(max_length=100)
    bot_usernamr = models.CharField(max_length=50)
    bot_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name
