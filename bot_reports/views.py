from django.shortcuts import render
from utils import now_timestamp
from .models import AdminLog, CustomerLog, ConfigLog


class Log:
    @classmethod
    def create_admin_log(cls, admin, action):
        AdminLog.objects.create(
            admin=admin,
            action=action,
            timestamp=now_timestamp()
        ).save()

    @classmethod
    def create_customer_log(cls, customer, action):
        CustomerLog.objects.create(
            customer=customer,
            action=action,
            timestamp=now_timestamp()
        ).save()

    @classmethod
    def create_config_log(cls, config, action):
        ConfigLog.objects.create(
            config=config,
            action=action,
            timestamp=now_timestamp()
        ).save()