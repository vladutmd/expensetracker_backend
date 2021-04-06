import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_1():
    user_1: User = User.objects.get(pk=1)
    assert user_1.email == "hi@there.com"
    assert user_1.password == "themostsecurepassword"
