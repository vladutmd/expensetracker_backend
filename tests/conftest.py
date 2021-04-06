import pytest
from django.contrib.auth import get_user_model
from djmoney.money import Money
from expenses.models import Category, Retailer, Transaction

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_1: User = User.objects.create(
            email="hi@there.com", password="themostsecurepassword"
        )
        retailer_1 = Retailer.objects.create(name="AmazIn", online=True, user=user_1)
        category_1 = Category.objects.create(
            name="Groceries", product_type="P", user=user_1
        )
        transaction_1 = Transaction.objects.create(
            amount=Money(420.00, "GBP"),
            name="Yoga Mat for Meditation",
            retailer=retailer_1,
            category=category_1,
            date="2021-04-20",
            transaction_type="E",
            recurring=False,
            user=user_1,
        )
