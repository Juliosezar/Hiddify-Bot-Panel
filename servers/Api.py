import requests
import uuid
from .models import Server
from utils import now_date

class HiddifyApi:
    @classmethod
    def create_config(cls, server_obj, config_obj, partition, comment=None):
        print("api")
        partition_dic = {
            "sellers_sub": server_obj.sellers_sub_uuid,
            "bot_sub": server_obj.bot_sub_uuid,
        }
        partition_uuid = str(partition_dic[partition])

        url = f"{server_obj.server_domain}/{server_obj.proxy_path}/api/v2/admin/user/"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            'Hiddify-API-Key': str(server_obj.admin_uuid)
        }
        if config_obj.days_limit == 0:
            days_limit = 5000
        else:
            days_limit = config_obj.days_limit
        payload = {
            "added_by_uuid": partition_uuid,
            "comment": comment,
            "current_usage_GB": 0,
            "enable": True,
            "is_active": True,
            "lang": "en",
            # "last_reset_time": now_date(),
            "mode": "no_reset",
            "name": config_obj.name,
            "package_days": 10000,
            "start_date": now_date(),
            "telegram_id": 0,
            "usage_limit_GB": 10000,
            "uuid": str(uuid.uuid4()),
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            print(response.json())
            print(response.status_code)
            return True
        except Exception as e:
            print(e)
            return False
