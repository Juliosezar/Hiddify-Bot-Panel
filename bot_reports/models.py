from django.db import models
from servers.models import BotConfigInfo, Customer


class BotErrorLog(models.Model):
    error = models.TextField()
    timestamp = models.IntegerField()


class ConfigLog(models.Model):
    config = models.ForeignKey(BotConfigInfo, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.IntegerField(default=1719482579)


class CustomerLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    action = models.TextField()
    timestamp = models.IntegerField(default=1719482579)


class AdminLog(models.Model):
    admin = models.CharField(max_length=15)
    action = models.TextField()
    timestamp = models.IntegerField(default=1719482579)

