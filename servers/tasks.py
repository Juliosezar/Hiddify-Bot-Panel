from celery import shared_task
from .Api import HiddifyApi
from .models import Server, BotEveryServer, BotConfigInfo
from utils import now_timestamp

@shared_task
def create_configs(conf_uuid):
    print("")
    config_obj = BotConfigInfo.objects.get(uuid=conf_uuid)

    for server in Server.objects.all():
        print(server.name)
        response = HiddifyApi.create_config(server, config_obj, "bot_sub")
        if response:
            BotEveryServer.objects.create(
                server=server,
                config=config_obj,
                usage_now=0,
                days_now=0,
                update_timestamp=now_timestamp(),
            )


@shared_task
def renew_configs():
    print("DFgsdfg")
    pass