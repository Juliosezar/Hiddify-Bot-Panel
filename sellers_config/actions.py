import uuid
from .models import SellersConfigInfo
from utils import generate_unique_name, now_timestamp
from sellers_finance.models import Payment
from .tasks import create_configs
class SellersActions:
    @classmethod
    def create_config(cls, days_limit, usage_limit, ip_limit, price, created_by, created_for):
        conf_uuid = uuid.uuid4()
        SellersConfigInfo.objects.create(
            name=generate_unique_name(),
            uuid=str(conf_uuid),
            seller=created_for,
            created_by=created_by,
            usage_limit=usage_limit,
            days_limit=days_limit,
            user_limit=ip_limit
        ).save()
        create_configs.delay(conf_uuid)
        Payment.objects.create(
            seller=created_for,
            amount=price,
            timestamp=now_timestamp(),
            created_by=created_by,
            description=f"{usage_limit if usage_limit != 0 else "∞"}GB - {days_limit if days_limit != 0 else "∞"}d - {ip_limit if ip_limit != 0 else "∞"}u"
        )
        return conf_uuid
