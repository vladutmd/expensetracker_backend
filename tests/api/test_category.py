import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Category


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient, category_factory):
    # let's create a category
    category: Category = category_factory()
    category_id: int = category.id
    get_category_url: str = reverse("retrieve_update_delete_category", args=[category_id])
    get_response: Response = api_client.get(
        get_category_url,
    )
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_own_category_with_token(api_client: APIClient, user_factory, category_factory):
    user = user_factory()
    category: Category = category_factory(user=user)
    category_id: int = category.id
    get_category_url: str = reverse("retrieve_update_delete_category", args=[category_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_category_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "id": category_id,
        "name": category.name,
        "product_type": category.product_type,
        "user": user.id,
        "slug": category.slug,
    }


@pytest.mark.django_db
def test_get_someone_elses_category_with_token(api_client: APIClient, user_factory, category_factory):
    user = user_factory()
    user_2 = user_factory()
    category: Category = category_factory(user=user_2)
    category_id: int = category.id
    get_category_url: str = reverse("retrieve_update_delete_category", args=[category_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_category_url,
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # let's now log in the client with user_2
    api_client.force_authenticate(user=user_2)
    get_response: Response = api_client.get(
        get_category_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "id": category_id,
        "name": category.name,
        "product_type": category.product_type,
        "user": user_2.id,
        "slug": category.slug,
    }


@pytest.mark.django_db
def test_update_category(api_client: APIClient, user_factory, category_factory):
    user = user_factory()
    category: Category = category_factory(user=user, name="original_nme")
    category_id: int = category.id
    category_url: str = reverse("retrieve_update_delete_category", args=[category_id])
    api_client.force_authenticate(user=user)
    response: Response = api_client.put(
        category_url,
        data={
            "name": "new_name",
            "product_type": category.product_type,
            "slug": category.slug,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    category.refresh_from_db()
    assert category.name == "new_name"

    # let's create a new user and see if we can change the user of this category
    user_2 = user_factory()
    response: Response = api_client.put(
        category_url,
        data={
            "name": category.name,
            "product_type": category.product_type,
            "user": user_2.id,
            "slug": category.slug,
        },
    )
    category.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert category.user == user
    # good, it did not change


@pytest.mark.django_db
def test_delete_category(api_client: APIClient, user_factory, category_factory):
    user = user_factory()
    category: Category = category_factory(user=user, name="gonna_have_to_go")
    category_id: int = category.id
    category_url: str = reverse("retrieve_update_delete_category", args=[category_id])
    api_client.force_authenticate(user=user)
    response: Response = api_client.delete(category_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(id=category_id)
