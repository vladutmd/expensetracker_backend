import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from expenses.models import Retailer

User = get_user_model()


@pytest.mark.django_db
def test_retailer_1():
    retailer_1 = Retailer.objects.get(pk=1)
    user_1 = User.objects.get(pk=1)
    assert retailer_1.name == "AmazIn"
    assert retailer_1.online
    assert retailer_1.user == user_1


@pytest.mark.django_db
def test_random_retailer_factory(retailer_factory):
    retailer = retailer_factory()
    assert retailer.online
    assert "AmazI" in retailer.name
    assert retailer.name[-1].isdigit()
    assert "@" in retailer.user.email


@pytest.mark.django_db
def test_offline_retailer_factory(retailer_factory):
    retailer = retailer_factory(online=False)
    assert "AmazI" in retailer.name
    assert retailer.name[-1].isdigit()
    assert "@" in retailer.user.email
    assert not retailer.online


@pytest.mark.django_db
def test_invalid_user(retailer_factory):
    with pytest.raises(ValueError) as exception_info:
        retailer_factory(user="invalid")
    assert exception_info.type == ValueError


@pytest.mark.django_db
def test_name_too_long(retailer_factory):
    with pytest.raises(DataError) as exception_info:
        retailer_factory(name="a" * 256)
    assert exception_info.type == DataError


@pytest.mark.django_db
def test_online_invalid_bool(retailer_factory):
    with pytest.raises(ValidationError) as exception_info:
        retailer_factory(online="Falsish")
    assert exception_info.type == ValidationError
