from django.contrib.auth import get_user_model
from django.db import models
from djmoney.models.fields import MoneyField


class Retailer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    # location = models.CharField(max_length=255)
    online = models.BooleanField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "retailer"
        verbose_name_plural = "retailers"
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="retailer_unique_name_per_user"),
            models.UniqueConstraint(fields=["slug", "user"], name="retailer_unique_slug_per_user"),
        ]

    def __str__(self):
        return f"{self.name} ({'Online' if self.online else 'Physical'})"

    def __repr__(self):
        return f"<Retailer: {self.name}>"


class Category(models.Model):
    PRODUCT_TYPES = (("P", "Physical"), ("E", "Electronic"))
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="category_unique_name_per_user"),
            models.UniqueConstraint(fields=["slug", "user"], name="category_unique_slug_per_user"),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()})"

    def __repr__(self):
        return f"<Category: {self.name}>"


class Transaction(models.Model):
    TRANSACTION_TYPES = (("E", "Expense"), ("I", "Income"))
    name = models.CharField(max_length=255)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency=None)
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    recurring = models.BooleanField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
