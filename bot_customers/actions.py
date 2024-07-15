from .models import Customer

class CustomerAction:
    @classmethod
    def create_custumer(cls, chat_id, first_name, username):
        if first_name:
            first_name = first_name[:20]
        else:
            first_name = ''
        Customer.objects.create(
            chat_id=chat_id,
            first_name=first_name,
            username=username,
        ).save()

    @classmethod
    def reload_custumer_info(cls, chat_id, first_name, username):
        if first_name:
            first_name = first_name[:20]
        else:
            first_name = ''
        custumer = Customer.objects.get(chat_id=chat_id)
        custumer.first_name = first_name
        custumer.username = username
        custumer.save()


    @classmethod
    def check_custumer_info(cls, chat_id, first_name, username):
        if Customer.objects.filter(chat_id=chat_id).exists():
            user = Customer.objects.get(chat_id=chat_id)
            if not (user.first_name == first_name and user.username == username):
                cls.reload_custumer_info(chat_id, first_name, username)
        else:
            cls.create_custumer(chat_id, first_name, username)
            return False
        return True


    @classmethod
    def change_custimer_temp_status(cls, chat_id, status):
        custumer_obj = Customer.objects.get(chat_id=chat_id)
        custumer_obj.temp_status = status
        custumer_obj.save()
