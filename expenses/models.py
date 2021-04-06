from django.db import models
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField


class Retailer(models.Model):
    name = models.CharField(max_length=255)
    # location = models.CharField(max_length=255)
    online = models.BooleanField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "retailer"
        verbose_name_plural = "retailers"


class Category(models.Model):
    PRODUCT_TYPES = (
        ('P', 'Physical'),
        ('E', 'Electronic')
    )
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPES)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('E', 'Expense'),
        ('I', 'Income')
    )
    amount = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency=None
    )
    name = models.CharField(max_length=255)
    retailer = models.ForeignKey(
        Retailer,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )
    date = models.DateField(
        auto_now=False,
        auto_now_add=False
    )
    transaction_type = models.CharField(
        max_length=1,
        choices=TRANSACTION_TYPES
    )
    recurring = models.BooleanField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
