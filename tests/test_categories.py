import pytest
from django.contrib.auth import get_user_model
from expenses.models import Category

User = get_user_model()


@pytest.mark.django_db
def test_category_1():
    category_1 = Category.objects.get(pk=1)
    user_1 = User.objects.get(pk=1)
    assert category_1.name == "Groceries"
    assert category_1.product_type == "P"
    assert category_1.user == user_1
