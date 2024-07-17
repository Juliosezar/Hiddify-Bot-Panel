from django.db import models
from bot_customers.models import Customer

class Server(models.Model):
    ID = models.PositiveIntegerField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=30, null=False, unique=True)
    proxy_path = models.CharField(max_length=30, null=True)
    port = models.IntegerField(null=True)
    server_domain = models.CharField(max_length=50, null=True, unique=True)
    fake_domain = models.CharField(max_length=50, null=True)
    admin_uuid = models.UUIDField(null=True)
    sellers_sub_uuid = models.UUIDField(null=True)
    bot_sub_uuid = models.UUIDField(null=True)
    active = models.BooleanField(default=True)
    old_iphone = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BotConfigInfo(models.Model):
    name = models.CharField(max_length=40, null=False)
    uuid = models.UUIDField(null=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20, default="BOT")
    renew_count = models.IntegerField(default=0)
    usage_limit = models.IntegerField(default=0)
    endtime_timestamp = models.PositiveIntegerField(null=True)
    user_limit = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.name


class BotInfinitCongisLimit(models.Model):
    config = models.OneToOneField(BotConfigInfo, on_delete=models.CASCADE)
    limit = models.IntegerField()


class BotEveryServer(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    config = models.ForeignKey(BotConfigInfo, on_delete=models.CASCADE)
    usage_now = models.PositiveIntegerField(null=True)
    days_now = models.PositiveIntegerField(null=True)
    update_timestamp = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.server.name + self.config.name


