import requests
import uuid
from .models import Server
from utils import now_date, now_timestamp

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
            if response.status_code == 200:
                print(response.json())
                print(response.status_code)
                return True
            else:
                print(response.status_code)
                return False
        except Exception as e:
            print(e)
            return False
