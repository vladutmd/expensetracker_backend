import logging

from rest_framework import serializers

from expenses.models import Category, Retailer

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    product_type = serializers.ChoiceField(choices=Category.PRODUCT_TYPES)

    class Meta:
        model = Category
        fields = ["name", "product_type", "user"]


class RetailerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    online = serializers.BooleanField()
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Retailer
        fields = ["name", "online", "user"]
