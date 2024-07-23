from django.db import models
from accounts.models import User


class SubSellrsRelation(models.Model):
    parent_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_seller")
    child_seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="child_seller")


class SellersPrices(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellerprice")
    usage_limit = models.PositiveIntegerField()
    expire_limit = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    user_limit = models.PositiveIntegerField(default=0)


class Payment(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellerpayment")
    amount = models.IntegerField()
    timestamp = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255)

