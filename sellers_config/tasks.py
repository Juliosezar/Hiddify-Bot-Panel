from celery import shared_task
from servers.Api import HiddifyApi
from servers.models import Server
from sellers_config.models import SellerConfigsEveryServerUsage, SellersConfigInfo
from utils import now_timestamp

@shared_task
def create_configs(conf_uuid):
    print("")
    config_obj = SellersConfigInfo.objects.get(uuid=conf_uuid)

    for server in Server.objects.all():
        print(server.name)
        response = HiddifyApi.create_config(server, config_obj, "sellers")
        if response:
            SellerConfigsEveryServerUsage.objects.create(
                server=server,
                config=config_obj,
                usage_now=0,
                update_timestamp=now_timestamp(),
            )


@shared_task
def renew_configs():
    print("DFgsdfg")
    pass