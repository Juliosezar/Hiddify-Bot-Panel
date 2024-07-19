from bot_customers.models import Customer
from .models import Prices, ConfirmPaymentQueue, ConfirmTamdidPaymentQueue
from bot_config.models import BotConfigInfo
from bot_finance.models import ConfirmPaymentQueue, ConfirmTamdidPaymentQueue, TamdidConfigQueue, CreateConfigQueue
from bot_finance.models import Customer
from .models import BotConfigInfo
from utils import generate_unique_name


class FinanceAction:
    @staticmethod
    def get_wallet_anount(chat_id):
        amount = Customer.objects.get(chat_id=chat_id).wallet
        return amount

    @staticmethod
    def add_to_wallet(chat_id, amount):
        wallet_obj = Customer.objects.get(chat_id=chat_id)
        wallet_obj.wallet = wallet_obj.wallet + amount
        wallet_obj.save()

    @staticmethod
    def get_expire_times():
        price_obj = Prices.objects.all()
        months = [m.expire_limit for m in price_obj]
        months = list(set(months))  # for delete same values
        return months

    @staticmethod
    def get_usage_and_prices_of_selected_month(month):
        price_obj = Prices.objects.filter(expire_limit=month)
        return price_obj

    @staticmethod
    def pay_config_before_img(chat_id, price, uuid):
        user_obj = Customer.objects.get(chat_id=chat_id)
        if ConfirmPaymentQueue.objects.filter(custumer=user_obj, status=0).exists():
            ConfirmPaymentQueue.objects.get(custumer=user_obj, status=0).delete()
        ConfirmPaymentQueue.objects.create(
            custumer=user_obj,
            config_price=price,
            pay_price=price - user_obj.wallet,
            status=0,
            config_in_queue=True,
            config_uuid=uuid,
        ).save()

    @staticmethod
    def pay_to_wallet_before_img(chat_id, price):
        user_obj = Customer.objects.get(chat_id=chat_id)
        if ConfirmPaymentQueue.objects.filter(custumer=user_obj, status=0).exists():
            ConfirmPaymentQueue.objects.get(custumer=user_obj, status=0).delete()
        ConfirmPaymentQueue.objects.create(
            custumer=user_obj,
            config_price=None,
            pay_price=price,
            status=0,
        ).save()

    @staticmethod
    def pay__tamdid__config_before_img(chat_id, price, uuid):
        config = BotConfigInfo.objects.get(config_uuid=uuid)
        user_obj = Customer.objects.get(chat_id=chat_id)
        if ConfirmTamdidPaymentQueue.objects.filter(config=config, status=0).exists():
            ConfirmTamdidPaymentQueue.objects.get(config=config, status=0).delete()
        ConfirmTamdidPaymentQueue.objects.create(
            config=config,
            config_price=price,
            pay_price=price - user_obj.wallet,
            status=0,
        ).save()

    @staticmethod
    def add_configs_to_queue_before_confirm(chat_id, config_uuid, usage_limit, expire_time, user_limit, price):
        user_obj = Customer.objects.get(chat_id=chat_id)
        if CreateConfigQueue.objects.filter(custumer=user_obj, pay_status=0).exists():
            CreateConfigQueue.objects.get(custumer=user_obj, pay_status=0).delete()
        config_name = generate_unique_name()
        CreateConfigQueue.objects.create(
            custumer=user_obj,
            config_uuid=config_uuid,
            config_name=config_name,
            usage_limit=usage_limit,
            expire_time=expire_time,
            user_limit=user_limit,
            price=price,
        ).save()

    @staticmethod
    def add_configs_to__tamdid__queue_before_confirm(config_uuid, usage_limit, expire_time, user_limit, price):
        config_info = BotConfigInfo.objects.get(config_uuid=config_uuid)
        if TamdidConfigQueue.objects.filter(config=config_info, pay_status=0).exists():
            TamdidConfigQueue.objects.get(config=config_info, pay_status=0).delete()

        TamdidConfigQueue.objects.create(
            config=config_info,
            usage_limit=usage_limit,
            expire_time=expire_time,
            user_limit=user_limit,
            price=price
        ).save()
