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
    sellers_single_uuid = models.UUIDField(null=True)
    sellers_sub_uuid = models.UUIDField(null=True)
    bot_single_uuid = models.UUIDField(null=True)
    bot_sub_uuid = models.UUIDField(null=True)
    active = models.BooleanField(default=True)
    old_iphone = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BotConfigInfo(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=False)
    uuid = models.UUIDField(null=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.join(f" / {self.server.name}")


class BotSubscriptionInfo(models.Model):
    name = models.CharField(max_length=40, null=False)
    uuid = models.UUIDField(null=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BotSubConfigsCreateStatus(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    subscription = models.ForeignKey(BotSubscriptionInfo, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=[(0, "in queue"), (1, "pending server"), (2, "done"), (-1, "error")])
    update_timestamp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subscription.name.join(f" / {self.server.name}")

