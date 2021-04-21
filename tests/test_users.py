import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


@pytest.mark.django_db
def test_user_1():
    user_1: User = User.objects.get(pk=1)
    assert isinstance(user_1, User)
    assert user_1.email == "hi@there.com"
    assert user_1.password == "themostsecurepassword"


@pytest.mark.django_db
def test_user_email(user_factory):
    user = user_factory()
    assert isinstance(user, User)
    assert "@" in user.email
    assert "user_" in user.username
    assert user.username[5].isdigit()


@pytest.mark.django_db
def test_user_factory_override_email(user_factory):
    user = user_factory(email="amazing_email@hmail.com")
    assert isinstance(user, User)
    assert user.email == "amazing_email@hmail.com"
