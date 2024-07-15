from django.db import models


class BotErrorLog(models.Model):
    error = models.TextField()
    timestamp = models.IntegerField()
