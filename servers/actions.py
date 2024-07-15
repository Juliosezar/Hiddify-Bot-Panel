from .Api import HiddifyApi
from bot_finance.models import ConfirmPaymentQueue, ConfirmTamdidPaymentQueue, TamdidConfigQueue, CreateConfigQueue
from bot_finance.models import Customer
from .models import BotConfigInfo
from utils import generate_unique_name
class BotAction:
    @classmethod
    def create_config_by_admins(cls, server_obj, name, usage_limit, days_limit, user_limit, comment):
        pass

    @classmethod
    def create_sub_by_admins(cls, server_obj, name, usage_limit, days_limit, user_limit, comment):
        pass

    @classmethod
    def create_sub_by_bot(cls, chatid, server_obj, name, usage_limit, days_limit, user_limit, comment):
        pass





class SellersAction:
    pass



class Tools:
    @classmethod
    def create_vless_text(cls):
        pass


class ActionQueue:
    pass