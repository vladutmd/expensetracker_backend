import pytest
from django.contrib.auth import get_user_model
from expenses.models import Retailer

User = get_user_model()


@pytest.mark.django_db
def test_retailer_1():
    retailer_1 = Retailer.objects.get(pk=1)
    user_1 = User.objects.get(pk=1)
    assert retailer_1.name == "AmazIn"
    assert retailer_1.online == True
    assert retailer_1.user == user_1
