import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Retailer


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient):
    list_retailer_url: str = reverse("view_and_create_retailers")
    list_response: Response = api_client.get(
        list_retailer_url,
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_retailers_with_token(api_client: APIClient, user_factory):
    email: str = "bobby@email.com"
    password: str = "smith"
    user = user_factory(email=email, password=password)
    list_retailer_url: str = reverse("view_and_create_retailers")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_retailer_url,
    )
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_retailers_with_token_actual_categories(
    api_client: APIClient, user_factory, retailer_factory
):
    email = "bobby@email.com"
    password = "smith"
    user = user_factory(email=email, password=password)
    _ = retailer_factory()
    _ = retailer_factory(user=user)
    list_retailer_url: str = reverse("view_and_create_retailers")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_retailer_url,
    )
    # only 1 should be available since the other one was created by a
    # different user
    assert (len(list_response.data)) == 1
    assert list_response.status_code == status.HTTP_200_OK
    # let's create another retailer
    _ = retailer_factory(user=user)
    # now there should be two returened
    list_response: Response = api_client.get(
        list_retailer_url,
    )
    assert (len(list_response.data)) == 2
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_retailer_without_authentication(api_client):
    list_retailer_url: str = reverse("view_and_create_retailers")
    data = {"name": "AbaP", "online": True, "slug": "abap"}
    list_response: Response = api_client.post(
        list_retailer_url, data=data, format="json"
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_retailer_with_authentication(api_client, user_factory):
    initial_count: int = Retailer.objects.all().count()
    user = user_factory()
    api_client.force_authenticate(user=user)
    list_retailer_url: str = reverse("view_and_create_retailers")

    data = {"name": "AbaP", "online": "True", "slug": "abap"}
    list_response: Response = api_client.post(
        list_retailer_url, data=data, format="json"
    )
    final_count: int = Retailer.objects.all().count()
    assert list_response.status_code == status.HTTP_201_CREATED
    assert final_count == initial_count + 1


@pytest.mark.django_db
def test_post_retailer_twice(api_client, user_factory):
    initial_count: int = Retailer.objects.count()
    user = user_factory()
    api_client.force_authenticate(user=user)
    list_retailer_url: str = reverse("view_and_create_retailers")

    data = {"name": "Ebup", "online": "True", "slug": "ebup"}
    list_response: Response = api_client.post(
        list_retailer_url, data=data, format="json"
    )
    final_count: int = Retailer.objects.count()
    assert list_response.status_code == status.HTTP_201_CREATED
    assert final_count == initial_count + 1

    # now let's try post it again
    second_list_response: Response = api_client.post(
        list_retailer_url, data=data, format="json"
    )
    assert second_list_response.status_code == status.HTTP_400_BAD_REQUEST
    json_response: dict[str, list[str]] = second_list_response.json()
    assert (
        "There is already a Retailer with this name for the current user"
        in json_response["non_field_errors"]
    )
    assert (
        "There is already a Retailer with this slug for the current user"
        in json_response["non_field_errors"]
    )
    # let's also assert that the count hasn't changed
    assert Retailer.objects.count() == final_count
