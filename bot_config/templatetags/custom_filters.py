from django import template
from bot_config.models import BotConfigInfo, BotInfinitCongisLimit
from django.conf import settings
import json
from persiantools.jdatetime import JalaliDateTime
import datetime, pytz
from bot_finance.models import CreateConfigQueue
from bot_finance.models import ConfirmPaymentQueue, ConfirmTamdidPaymentQueue
from bot_config.models import BotConfigsEveryServerUsage
from utils import now_timestamp


register = template.Library()

with open(settings.BASE_DIR / "settings.json", "r") as f:
    UNLIMIT_LIMIT = json.load(f)["unlimit_limit"]


@register.filter
def expired(days_limit, start_timastamp):
    if days_limit == 0:
        return False
    if ((start_timastamp + (days_limit * 86400)) - now_timestamp()) < 0:
        return True
    return False

@register.filter
def remain_days(days_limit, start_timastamp):
    if start_timastamp:
        remain =  ((start_timastamp + (days_limit * 86400)) - now_timestamp()) / 86400
    else:
        remain = days_limit
    hour = int((abs(remain) % 1) * 24)
    day = abs(int(remain))
    text = f"{day}d {hour}h"
    print(remain)
    if remain < 0:
        text += " ago"
    return text



@register.filter
def bot_add_usages(uuid):
    add = 0
    for i in BotConfigsEveryServerUsage.objects.filter(config__uuid=uuid):
        add += i.usage_now
    return add

@register.filter
def price(amount):
    return f"{amount:,}"


@register.filter(name='percent')
def percent_usage(value, arg):
    return int(value / arg * 100)


@register.filter(name="dh")
def day_and_hour(value):
    hour = int((abs(value) % 1) * 24)
    day = abs(int(value))
    return f"{day}d {hour}h"


@register.filter(name="break_name")
def break_name(value):
    if BotConfigInfo.objects.filter(config_name=value).exists():
        return f'{value} 🤖'
    elif '@' in value:
        return False
    return value


@register.filter(name="config_seved")
def config_seved(value):
    if BotConfigInfo.objects.filter(config_uuid=value).exists():
        return True
    return False


@register.filter(name="infinit_limit")
def infinit_limit(value):
    config_info = BotConfigInfo.objects.filter(uuid=value)
    if config_info.exists():
        if BotInfinitCongisLimit.objects.filter(config__uuid=value).exists():
            return BotInfinitCongisLimit.objects.get(config__uuid=value).limit
        else:
            return "Not Set"
    return None


@register.filter(name="timestamp")
def timestamp(value):
    return JalaliDateTime.fromtimestamp(value, pytz.timezone("Asia/Tehran")).strftime("%c")


@register.filter(name="get_server")
def get_server(value):
    if CreateConfigQueue.objects.filter(config_uuid=value).exists():
        return CreateConfigQueue.objects.get(config_uuid=value).server.server_name
    else:
        return "----"


def status(value):
    if value == 1:
        return "waiting for confirm ⏳"
    elif value == 2:
        return "first confirm ☑️"
    elif value == 3:
        return "confirmed ✅"
    else:
        return "Denyed ❌"


def config_name(uuidd):
    if BotConfigInfo.objects.filter(config_uuid=uuidd).exists():
        return BotConfigInfo.objects.get(config_uuid=uuidd).config_name
    else:
        return "----"


@register.filter(name="paylog")
def paylog(id: dict):
    if "buy" in list(id.keys()):
        obj = ConfirmPaymentQueue.objects.get(id=id["buy"])
        if obj.config_in_queue:
            return f"Buy / {config_name(obj.config_uuid)} / {price(obj.pay_price)}T / {status(obj.status)}"
        else:
            return f"Wallet / {price(obj.pay_price)}T / {status(obj.status)}"
    else:
        obj = ConfirmTamdidPaymentQueue.objects.get(id=id["tamdid"])
        return f"Tamdid / {obj.config.config_name} / {price(obj.pay_price)}T / {status(obj.status)}"


@register.filter(name="get_user")
def get_user(id: dict):
    if "buy" in list(id.keys()):
        obj = ConfirmPaymentQueue.objects.get(id=id["buy"])
        return obj.custumer.userid
    else:
        obj = ConfirmTamdidPaymentQueue.objects.get(id=id["tamdid"])
        return obj.config.chat_id.userid
