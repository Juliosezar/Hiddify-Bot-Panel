from django.db import models
from bot_customers.models import Customer
from servers.models import Server


class BotConfigInfo(models.Model):
    name = models.CharField(max_length=40, null=False)
    uuid = models.UUIDField(null=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20, default="BOT")
    renew_count = models.IntegerField(default=0)
    usage_limit = models.IntegerField(default=0)
    days_limit = models.IntegerField(default=0)
    start_timestamp = models.PositiveIntegerField(null=True)
    user_limit = models.PositiveIntegerField(default=0)
    enable = models.BooleanField(default=True)
    update = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class BotInfinitCongisLimit(models.Model):
    config = models.OneToOneField(BotConfigInfo, on_delete=models.CASCADE)
    limit = models.IntegerField()


class BotConfigsEveryServerUsage(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    config = models.ForeignKey(BotConfigInfo, on_delete=models.CASCADE)
    usage_now = models.FloatField(default=0)
    update_timestamp = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.server.name + self.config.name

