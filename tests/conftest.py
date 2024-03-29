import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from djmoney.money import Money
from pytest_factoryboy import register
from rest_framework.test import APIClient, APIRequestFactory

from expenses.models import Category, Retailer, Transaction
from tests.factories import (
    CategoryFactory,
    RetailerFactory,
    TransactionFactory,
    UserFactory,
)

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_1: User = User.objects.create(
            username="hi",
            email="hi@there.com",
            password="themostsecurepassword",
            is_active=True,
        )
        EmailAddress.objects.create(email=user_1.email, verified=True, primary=True, user=user_1)
        retailer_1 = Retailer.objects.create(name="AmazIn", online=True, user=user_1)
        category_1 = Category.objects.create(name="Groceries", product_type="P", user=user_1)
        _ = Transaction.objects.create(
            amount=Money(420.00, "GBP"),
            name="Yoga Mat for Meditation",
            retailer=retailer_1,
            category=category_1,
            date="2021-04-20",
            transaction_type="E",
            recurring=False,
            user=user_1,
        )


register(UserFactory)
register(RetailerFactory)
register(CategoryFactory)
register(TransactionFactory)

# create specific versions
register(
    UserFactory,
    "same_user",
    username="specific_user",
    email="specific_user@email.com",
    password="specific_password",
)
register(RetailerFactory, "same_user_retailer")
register(CategoryFactory, "same_user_category")
register(TransactionFactory, "same_user_transaction")


@pytest.fixture
def same_user_retailer__user(same_user):
    return same_user


@pytest.fixture
def same_user_category__user(same_user):
    return same_user


@pytest.fixture
def same_user_transaction__user(same_user):
    return same_user


@pytest.fixture
def same_user_transaction__retailer(same_user_retailer):
    return same_user_retailer


@pytest.fixture
def same_user_transaction__category(same_user_category):
    return same_user_category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_reqfactory():
    return APIRequestFactory()
