import pytest
from django.contrib.auth import get_user_model
from expenses.models import Transaction, Category, Retailer
from djmoney.money import Money

User = get_user_model()


@pytest.mark.django_db
def test_transaction_1():
    # get the Category, Retailer and User from the database
    category_1 = Category.objects.get(pk=1)
    retailer_1 = Retailer.objects.get(pk=1)
    user_1 = User.objects.get(pk=1)
    # get the transaction and test it
    transaction_1 = Transaction.objects.get(pk=1)
    assert transaction_1.amount == Money(420.00, "GBP")
    assert transaction_1.name == "Yoga Mat for Meditation"
    assert transaction_1.retailer == retailer_1
    assert transaction_1.category == category_1
    assert transaction_1.date.isoformat() == "2021-04-20"
    assert transaction_1.transaction_type == "E"
    assert transaction_1.recurring == False
    assert transaction_1.user == user_1