import requests
import uuid
from .models import Server


class HiddifyApi:
    @classmethod
    def create_config(cls, server_obj, partition, name, usage_limit, days_limit, comment=None):
        partition_dic = {
            "sellers_single": server_obj.sellers_single_uuid,
            "sellers_sub": server_obj.sellers_sub_uuid,
            "bot_single": server_obj.bot_single_uuid,
            "bot_sub": server_obj.bot_sub_uuid,
        }
        partition_uuid = str(partition_dic[partition])

        url = f"{server_obj.server_domain}/{server_obj.proxy_path}/api/v2/admin/user/"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Hiddify-API-Key': str(server_obj.admin_uuid)
        }

        payload = {
            "added_by_uuid": partition_uuid,
            "comment": comment,
            "current_usage_GB": 0,
            "enable": True,
            "is_active": True,
            "lang": "en",
            # "last_reset_time": null,
            "mode": "no_reset",
            "name": name,
            "package_days": days_limit,
            "start_date": "2019-08-24",
            "telegram_id": 0,
            "usage_limit_GB": usage_limit,
            "uuid": str(uuid.uuid4()),
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            print(response.json())
            print(response.status_code)
        except Exception as e:
            print(e)
