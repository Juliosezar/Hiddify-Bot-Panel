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
    last_update = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name



