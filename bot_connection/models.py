from django.db import models
from bot_customers.models import Customer


class SendMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(choices=((10, 'Succes'), (0, 'Created'), (1, 'Pending'), (-1, 'Faild'),
                                          (-10, 'Cancelled'), (-2, 'Banned')), default=0)
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.status) + " / " + self.message[:40]
