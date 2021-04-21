import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from djmoney.money import Money
from expenses.models import Category, Retailer, Transaction
from moneyed.classes import CurrencyDoesNotExist

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


@pytest.mark.django_db
def test_transaction_foreignkeys(transaction_factory):
    transaction = transaction_factory()
    assert isinstance(transaction.retailer, Retailer)
    assert isinstance(transaction.category, Category)
    assert isinstance(transaction.user, User)


@pytest.mark.parametrize("same_user_transaction__name", ["Transaction_420"])
@pytest.mark.django_db
def test_transaction_factory_specific(same_user_transaction, same_user):
    assert same_user_transaction.name == "Transaction_420"
    assert same_user_transaction.user == same_user
    assert same_user_transaction.category.user == same_user_transaction.user
    assert same_user_transaction.retailer.user == same_user_transaction.user


@pytest.mark.django_db
def test_transaction_name_too_long(transaction_factory):
    with pytest.raises(DataError) as exception_info:
        transaction_factory(name="a" * 256)
    assert exception_info.type == DataError


@pytest.mark.django_db
def test_transaction_fake_currency(transaction_factory):
    with pytest.raises(CurrencyDoesNotExist) as exception_info:
        transaction_factory(amount=Money(23.023, "ABC"))
    assert exception_info.type == CurrencyDoesNotExist


@pytest.mark.django_db
def test_transaction_retailer_invalid(transaction_factory):
    with pytest.raises(ValueError) as exception_info:
        transaction_factory(retailer="Not a retailer instance")
    assert exception_info.type == ValueError


@pytest.mark.django_db
def test_transaction_invalid_date(transaction_factory):
    with pytest.raises(ValidationError) as exception_info:
        transaction_factory(date="2040-15-42")
    assert exception_info.type == ValidationError


@pytest.mark.django_db
def test_transaction_invalid_type(transaction_factory):
    with pytest.raises(DataError) as exception_info:
        transaction_factory(transaction_type="EX")
    assert exception_info.type == DataError


@pytest.mark.django_db
def test_transaction_recurring_bool(transaction_factory):
    with pytest.raises(ValidationError) as exception_info:
        transaction_factory(recurring="no")
    assert exception_info.type == ValidationError


@pytest.mark.django_db
def test_transaction_invalid_user(transaction_factory):
    with pytest.raises(ValueError) as exception_info:
        transaction_factory(user="Batboy")
    assert exception_info.type == ValueError


@pytest.mark.xfail
@pytest.mark.django_db
def test_transaction_user_instances(transaction_factory):
    transaction = transaction_factory()
    assert transaction.retailer.user == transaction.category.user
    assert transaction.retailer.user == transaction.user
