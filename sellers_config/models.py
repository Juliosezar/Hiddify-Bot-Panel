from django.db import models
from accounts.models import User
from servers.models import Server


class SellersConfigInfo(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(unique=True, primary_key=True)
    bot_user = models.PositiveIntegerField(null=True)
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="seller")
    usage_limit = models.IntegerField(default=0)
    days_limit = models.IntegerField(default=0)
    user_limit = models.IntegerField(default=0)
    start_timestamp = models.IntegerField(null=True)
    enable = models.BooleanField(default=True)
    renew_count = models.PositiveIntegerField(default=0)
    update = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class SellerInfinitCongisLimit(models.Model):
    config = models.OneToOneField(SellersConfigInfo, on_delete=models.CASCADE)
    limit = models.IntegerField()


class SellerConfigsEveryServerUsage(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    config = models.ForeignKey(SellersConfigInfo, on_delete=models.CASCADE)
    usage_now = models.FloatField(default=0)
    update_timestamp = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.server.name + self.config.name

