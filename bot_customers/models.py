from django.db import models


class Customer(models.Model):
    chatid = models.IntegerField(primary_key=True, unique=True, editable=False)
    first_name = models.CharField(max_length=25)
    username = models.CharField(max_length=32, null=True)
    wallet = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)

    def __str__(self):
        return self.chatid
