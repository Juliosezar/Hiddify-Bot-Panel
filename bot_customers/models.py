from django.db import models


class Customer(models.Model):
    chat_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=25)
    username = models.CharField(max_length=32, null=True)
    wallet = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)
    test_config = models.BooleanField(default=False)
    temp_status = models.CharField(max_length=30, default="normal")
    pay_temp_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.chat_id

