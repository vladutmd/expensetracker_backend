import logging

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from expenses.api.fields import UserSpecificSlugRelatedField

from expenses.models import Category, Retailer, Transaction
from djmoney.contrib.django_rest_framework import MoneyField
from moneyed import CURRENCIES

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    product_type = serializers.ChoiceField(choices=Category.PRODUCT_TYPES)
    slug = serializers.CharField(max_length=255)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Category
        fields = ["name", "product_type", "user", "slug"]
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=fields
            )
        ]


class RetailerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    online = serializers.BooleanField()
    slug = serializers.CharField(max_length=255)
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Retailer
        fields = ["name", "online", "user", "slug"]
        validators = [
            UniqueTogetherValidator(
                queryset=Retailer.objects.all(),
                fields=fields
            )
        ]


class TransactionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    amount = MoneyField(max_digits=14, decimal_places=2)
    amount_currency = serializers.ChoiceField(choices=CURRENCIES)
    retailer = UserSpecificSlugRelatedField(many=False, read_only=False, slug_field='slug', queryset=Retailer.objects)
    category = serializers.StringRelatedField(
        read_only=True,
    )
    category = UserSpecificSlugRelatedField(many=False, read_only=False, slug_field='slug', queryset=Category.objects)
    date = serializers.DateField()
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES)
    recurring = serializers.BooleanField()
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Transaction
        fields = ["name", "amount", "amount_currency", "retailer", "category", "date", "transaction_type", "recurring", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Transaction.objects.all(),
                fields=fields
            )
        ]
