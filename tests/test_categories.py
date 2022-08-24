import pytest
from django.contrib.auth import get_user_model
from django.db.utils import DataError, IntegrityError

from expenses.models import Category

User = get_user_model()


@pytest.mark.django_db
def test_category_1():
    category_1 = Category.objects.get(pk=1)
    user_1 = User.objects.get(pk=1)
    assert category_1.name == "Groceries"
    assert category_1.product_type == "P"
    assert category_1.user == user_1


@pytest.mark.django_db
def test_random_category_factory(category_factory):
    category = category_factory()
    assert category.product_type == "P"
    assert "Category_" in category.name
    assert category.name[-1].isdigit()
    assert "@" in category.user.email


@pytest.mark.django_db
def test_electronic_category_factory(category_factory):
    category = category_factory(product_type="E")
    assert category.product_type == "E"
    assert "Category_" in category.name
    assert category.name[-1].isdigit()
    assert "@" in category.user.email


@pytest.mark.django_db
def test_invalid_user(category_factory):
    with pytest.raises(ValueError) as exception_info:
        category_factory(user="invalid")
    assert exception_info.type == ValueError


@pytest.mark.django_db
def test_name_too_long(category_factory):
    with pytest.raises(DataError) as exception_info:
        category_factory(name="a" * 256)
    assert exception_info.type == DataError


@pytest.mark.django_db
def test_cannot_create_two_categories_with_same_slug_one_user(
    category_factory, user_factory
):
    user = user_factory()
    _ = category_factory(slug="hi-there", user=user)
    with pytest.raises(IntegrityError) as exception_info:
        category_factory(slug="hi-there", user=user)
    assert exception_info.type == IntegrityError
