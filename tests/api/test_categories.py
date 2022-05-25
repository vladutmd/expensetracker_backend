import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Category


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient):
    list_category_url: str = reverse("view_and_create_categories")
    list_response: Response = api_client.get(
        list_category_url,
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_categories_with_token(api_client: APIClient, user_factory):
    email: str = "bobby@email.com"
    password: str = "smith"
    user = user_factory(email=email, password=password)
    list_category_url: str = reverse("view_and_create_categories")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_category_url,
    )
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_categories_with_token_actual_categories(
    api_client: APIClient, user_factory, category_factory
):
    email = "bobby@email.com"
    password = "smith"
    user = user_factory(email=email, password=password)
    _ = category_factory()
    _ = category_factory(user=user)
    list_category_url: str = reverse("view_and_create_categories")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_category_url,
    )
    # only 1 should be available since the other one was created by a
    # different user
    assert (len(list_response.data)) == 1
    assert list_response.status_code == status.HTTP_200_OK
    # let's create another category
    _ = category_factory(user=user)
    # now there should be two returened
    list_response: Response = api_client.get(
        list_category_url,
    )
    assert (len(list_response.data)) == 2
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_category_without_authentication(api_client):
    list_category_url: str = reverse("view_and_create_categories")
    data = {"name": "Groceries", "product_type": "P", "slug": "groceries"}
    list_response: Response = api_client.post(
        list_category_url, data=data, format="json"
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_category_with_authentication(api_client, user_factory):
    initial_count: int = Category.objects.all().count()
    user = user_factory()
    api_client.force_authenticate(user=user)
    list_category_url: str = reverse("view_and_create_categories")

    data = {"name": "Groceries", "product_type": "P", "slug": "groceries"}
    list_response: Response = api_client.post(
        list_category_url, data=data, format="json"
    )
    final_count: int = Category.objects.all().count()
    assert list_response.status_code == status.HTTP_201_CREATED
    assert final_count == initial_count + 1


@pytest.mark.django_db
def test_post_category_twice(api_client, user_factory):
    initial_count: int = Category.objects.all().count()
    user = user_factory()
    api_client.force_authenticate(user=user)
    list_category_url: str = reverse("view_and_create_categories")

    data = {"name": "Entertainment", "product_type": "E", "slug": "entertainment"}
    list_response: Response = api_client.post(
        list_category_url, data=data, format="json"
    )
    final_count: int = Category.objects.all().count()
    assert list_response.status_code == status.HTTP_201_CREATED
    assert final_count == initial_count + 1

    # now let's try post it again
    second_list_response: Response = api_client.post(
        list_category_url, data=data, format="json"
    )
    assert second_list_response.status_code == status.HTTP_400_BAD_REQUEST
    json_response: dict[str, list[str]] = second_list_response.json()
    assert "The fields name, product_type, user, slug must make a unique set." in json_response["non_field_errors"]
    # let's also assert that the count hasn't changed
    assert Category.objects.count() == final_count