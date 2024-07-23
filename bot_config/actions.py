from bot_finance.models import TamdidConfigQueue, CreateConfigQueue, UserActiveOffCodes
from bot_finance.models import Customer
from bot_config.models import BotConfigInfo, BotInfinitCongisLimit
from utils import generate_unique_name, now_timestamp
import uuid
from bot_finance.actions import FinanceAction
from django.conf import settings
import json
from bot_reports.views import Log
from bot_config.tasks import create_configs, renew_configs


class BotAction:
    @classmethod
    def save_config_info(cls, config_name, config_uuid, chat_id, price, usege_limit, days_limit, user_limit, paid=True, created_by='Bot'):
        if chat_id:
            customer = Customer.objects.get(chat_id=chat_id)
        else:
            customer = None

        BotConfigInfo.objects.create(
            name=config_name,
            uuid=config_uuid,
            customer=customer,
            created_by=created_by,
            paid=paid,
            price=price,
            user_limit=user_limit,
            usage_limit=usege_limit,
            days_limit=days_limit,
            update=now_timestamp()
        ).save()

    @classmethod
    def change_config_info(cls, config_uuid, price, paid):
        if BotConfigInfo.objects.filter(uuid=config_uuid).exists():
            config_info = BotConfigInfo.objects.get(uuid=config_uuid)
            config_info.renew_count += 1
            config_info.price = price
            config_info.paid = paid
            config_info.save()

    @classmethod
    def create_config_from_queue(cls, config_uuid):
        from bot_connection.command_runer import CommandRunner
        config_queue_obj = CreateConfigQueue.objects.get(config_uuid=config_uuid)
        config_queue_obj.sent_to_user = 1
        config_queue_obj.save()
        cls.save_config_info(config_queue_obj.config_name, config_queue_obj.config_uuid,
                             config_queue_obj.custumer.chat_id,config_queue_obj.usage_limit, config_queue_obj.expire_time, config_queue_obj.user_limit,
                             config_queue_obj.price)
        create_configs.delay(config_uuid)
        if UserActiveOffCodes.objects.filter(custumer=config_queue_obj.custumer, used=False).exists():
            off_obj = UserActiveOffCodes.objects.get(custumer=config_queue_obj.custumer, used=False)
            off_obj.used = True
            off_obj.save()
        FinanceAction.add_to_wallet(config_queue_obj.custumer.chat_id, -1 * config_queue_obj.price)
        config_queue_obj.sent_to_user = 3

        Tools.send_config_to_user(config_queue_obj.custumer.chat_id, config_uuid, config_queue_obj.config_name)
        if config_queue_obj.usage_limit == 0:
            Tools.set_unlimit_limit(config_uuid, config_queue_obj.user_limit, int(config_queue_obj.expire_time / 30))
            CommandRunner.send_infinit_notification(config_queue_obj.custumer.chat_id, config_queue_obj.user_limit, int(config_queue_obj.expire_time / 30))
        Log.create_config_log(BotConfigInfo.objects.get(uuid=config_uuid),
                              f"➕ Create by \"Bot\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")
        Log.create_admin_log("Bot",
                             f"➕ Create \"{config_queue_obj.config_name}\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")
        Log.create_customer_log(Customer.objects.get(chat_id=config_queue_obj.custumer.chat_id),
                                f"➕ Create \"{config_queue_obj.config_name}\" by \"Bot\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")

    @classmethod
    def create_config_from_wallet(cls, chat_id, days_limit, usage_limit, user_limit, price):
        from bot_connection.command_runer import CommandRunner
        conf_uuid = str(uuid.uuid4())
        config_name = generate_unique_name()
        cls.save_config_info(config_name, conf_uuid, chat_id, price, usage_limit, days_limit, user_limit)
        create_configs.delay(conf_uuid)
        if UserActiveOffCodes.objects.filter(custumer__chat_id=chat_id, used=False).exists():
            off_obj = UserActiveOffCodes.objects.get(custumer__chat_id=chat_id, used=False)
            off_obj.used = True
            off_obj.save()
        FinanceAction.add_to_wallet(chat_id, -1 * price)
        Tools.send_config_to_user(chat_id, conf_uuid, config_name)
        if usage_limit == 0:
            Tools.set_unlimit_limit(conf_uuid, user_limit, days_limit)
            CommandRunner.send_infinit_notification(chat_id, user_limit, days_limit)
        Log.create_config_log(BotConfigInfo.objects.get(uuid=conf_uuid),
                              f"➕ Create by \"Bot\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        Log.create_admin_log("Bot",
                             f"➕ Create \"{config_name}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {price}T)")
        Log.create_customer_log(Customer.objects.get(chat_id=chat_id),
                                f"➕ Create \"{config_name}\" by \"Bot\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        return True

    @classmethod
    def create_config_by_admins(cls, days_limit, usage_limit, user_limit, price, paid, created_by):
        conf_uuid = uuid.uuid4()
        config_name = generate_unique_name()
        create_configs.delay(conf_uuid)
        cls.save_config_info(config_name, conf_uuid, None, price, usage_limit, days_limit, user_limit, paid, created_by)
        if usage_limit == 0:
            Tools.set_unlimit_limit(conf_uuid, user_limit, int(days_limit / 30))
        Log.create_config_log(BotConfigInfo.objects.get(uuid=conf_uuid),
                              f"➕ Create by \"{created_by}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        Log.create_admin_log(created_by,
                             f"➕ Create \"{config_name}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        return str(conf_uuid)



    @classmethod
    def tamdid_config_from_queue(cls, config_uuid, by_celery=False):
        from bot_connection.command_runer import CommandRunner
        config_queue_obj = TamdidConfigQueue.objects.get(config__config_uuid=config_uuid, sent_to_user=0)
        config_queue_obj.sent_to_user = 1
        config_queue_obj.save()
        renew_configs.delay()
        if UserActiveOffCodes.objects.filter(custumer=config_queue_obj.config.customer, used=False).exists():
            off_obj = UserActiveOffCodes.objects.get(custumer=config_queue_obj.config.customer, used=False)
            off_obj.used = True
            off_obj.save()
        FinanceAction.add_to_wallet(config_queue_obj.config.customer.chat_id, -1 * config_queue_obj.price)
        config_queue_obj.sent_to_user = 3
        cls.change_config_info(config_queue_obj.config.config_uuid, config_queue_obj.price, True)
        if config_queue_obj.usage_limit == 0:
            Tools.set_unlimit_limit(config_uuid, config_queue_obj.user_limit, int(config_queue_obj.expire_time / 30))
            CommandRunner.send_infinit_notification(config_queue_obj.config.customer.chat_id, config_queue_obj.user_limit, int(config_queue_obj.expire_time / 30))
        CommandRunner.send_msg_to_user(config_queue_obj.config.customer.chat_id,
                                       f"✅ سرویس {config_queue_obj.config.config_name} تمدید شد. از بخش (سرویس های من) در منوی اصلی میتوانید وضعیت سرویس خود را مشاهده کنید.")
        Log.create_config_log(config_queue_obj.config,
                              f"🔃 Renew by \"Bot\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")
        Log.create_admin_log("Bot",
                             f"🔃 Renew \"{config_queue_obj.config.config_name}\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")
        Log.create_customer_log(config_queue_obj.config.customer,
                                f"🔃 Renew \"{config_queue_obj.config.config_name}\" by \"Bot\" ({config_queue_obj.usage_limit}GB - {config_queue_obj.expire_time}day - {config_queue_obj.user_limit}Ip - {int(config_queue_obj.price / 1000)}T)")

    @classmethod
    def tamdid_config_from_wallet(cls, config_uuid, days_limit, usage_limit, user_limit, price):
        from bot_connection.command_runer import CommandRunner
        config_obj = BotConfigInfo.objects.get(uuid=config_uuid)
        renew_configs.delay()
        if UserActiveOffCodes.objects.filter(custumer=config_obj.customer, used=False).exists():
            off_obj = UserActiveOffCodes.objects.get(custumer=config_obj.customer, used=False)
            off_obj.used = True
            off_obj.save()
        cls.change_config_info(config_uuid, price, True)
        FinanceAction.add_to_wallet(config_obj.customer.chat_id, -1 * price)
        if usage_limit == 0:
            Tools.set_unlimit_limit(config_uuid, user_limit, days_limit)
            CommandRunner.send_infinit_notification(config_obj.customer.chat_id, user_limit, days_limit)
        CommandRunner.send_msg_to_user(config_obj.customer.chat_id,f"✅ سرویس {config_obj.config_name} تمدید شد. از بخش (سرویس های من) در منوی اصلی میتوانید وضعیت سرویس خود را مشاهده کنید.")
        Log.create_config_log(config_obj,f"🔃 Renew by \"Bot\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        Log.create_admin_log("Bot",f"🔃 Renew \"{config_obj.config_name}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        Log.create_customer_log(config_obj.customer,f"🔃 Renew \"{config_obj.config_name}\" by \"Bot\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        config_obj.renew_count += 1
        config_obj.price = True
        config_obj.save()
        return True


    @classmethod
    def tamdid_config_by_admins(cls, config_uuid, days_limit, usage_limit, user_limit, price, paid, by_admin):
        from bot_connection.command_runer import CommandRunner

        conf = BotConfigInfo.objects.get(uuid=config_uuid)
        renew_configs.delay()
        cls.change_config_info(config_uuid, price, paid)
        if usage_limit == 0:
            Tools.set_unlimit_limit(config_uuid, user_limit, int(days_limit / 30))
        Log.create_config_log(conf,f"🔃 Renew \"{conf.config_name}\" by \"{by_admin}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        Log.create_admin_log(by_admin,f"🔃 Renew \"{conf.config_name}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
        if conf.customer:
            CommandRunner.send_msg_to_user(conf.customer.chat_id,
                                           f" ✅ سرویس {conf.config_name} توسط ادمین تمدید شد. از بخش (سرویس های من) در منوی اصلی میتوانید وضعیت سرویس خود را مشاهده کنید. ")
            Log.create_customer_log(conf.customer,f"🔃 Renew \"{conf.config_name}\" by \"{by_admin}\" ({usage_limit}GB - {days_limit}day - {user_limit}Ip - {int(price / 1000)}T)")
            if usage_limit == 0:
                CommandRunner.send_infinit_notification(conf.customer.chat_id, user_limit, int(days_limit / 30))
        return {'config_name': conf.config_name, 'config_uuid': config_uuid}


class Tools:
    @classmethod
    def create_vless_text(cls, config_uuid, config_name):
        vless = ('📡 کانفیگ شما:' '\n\n'
                 f"```\nlink\n```"
                 '\n' '💠 برای کپی کردن کانفیگ روی دکمه <<کپی کردن کد>> (Copy Code) کلیک کنید.'
                 )
        return vless

    @classmethod
    def send_config_to_user(cls, chat_id, config_uuid, config_name):
        from bot_connection.command_runer import CommandRunner
        vless = cls.create_vless_text(config_uuid, config_name)
        CommandRunner.send_msg_to_user(chat_id, vless, keyboard=[{'text': 'دریافت QRcode', 'callback_data': f'QRcode<~>{config_uuid}'}])

    @classmethod
    def set_unlimit_limit(cls, config_uuid, iplimit, month):
        with open(settings.BASE_DIR / "settings.json", "r") as f:
            data = json.load(f)["unlimit_limit"]
        if (month in [1, 2, 3]) and (iplimit in [1, 2]):
            limit = data[f"{iplimit}u"][f"{month}m"]
        else:
            iplimit = max(1, min(iplimit, 2))
            month = max(1, min(month, 3))
            limit = data[f"{iplimit}u"][f"{month}m"]
        if BotInfinitCongisLimit.objects.filter(config__uuid=config_uuid).exists():
            obj = BotInfinitCongisLimit.objects.get(config__uuid=config_uuid)
            obj.limit = limit
            obj.save()
        else:
            BotInfinitCongisLimit.objects.create(config=BotConfigInfo.objects.get(uuid=config_uuid), limit=limit).save()
