import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Category, Retailer, Transaction


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient):
    list_transaction_url: str = reverse("view_and_create_transactions")
    list_response: Response = api_client.get(
        list_transaction_url,
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_transactions_with_token(api_client: APIClient, user_factory):
    email: str = "bobby@email.com"
    password: str = "smith"
    user = user_factory(email=email, password=password)
    list_transaction_url: str = reverse("view_and_create_transactions")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_transaction_url,
    )
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_transactions_with_token_actual_transactions(
    api_client: APIClient, user_factory, transaction_factory
):
    email = "bobby@email.com"
    password = "smith"
    user = user_factory(email=email, password=password)
    _ = transaction_factory()
    _ = transaction_factory(user=user)
    list_transaction_url: str = reverse("view_and_create_transactions")
    api_client.force_authenticate(user=user)
    list_response: Response = api_client.get(
        list_transaction_url,
    )
    # only 1 should be available since the other one was created by a
    # different user
    assert (len(list_response.data)) == 1
    assert list_response.status_code == status.HTTP_200_OK
    # let's create another category
    _ = transaction_factory(user=user)
    # now there should be two returened
    list_response: Response = api_client.get(
        list_transaction_url,
    )
    assert (len(list_response.data)) == 2
    assert list_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_transaction_without_authentication(api_client):
    list_transaction_url: str = reverse("view_and_create_transactions")
    data = {
        "name": "lala", "amount": "120.23", "amount_currency": "XYZ", "retailer": "Ret", "catgory": "cat", "date": "2022-05-23", "transaction_type": "E", "recurring": "false", "user": 1,
    }
    list_response: Response = api_client.post(
        list_transaction_url, data=data, format="json"
    )
    assert list_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_transaction_with_authentication(api_client, user_factory, category_factory, retailer_factory):
    initial_count: int = Transaction.objects.count()
    # let's create a category and a retailer
    user = user_factory()
    category: Category = category_factory(slug="unique_category", user=user)
    retailer: Retailer = retailer_factory(slug="unique_retailer", user=user)


    api_client.force_authenticate(user=user)
    list_transaction_url: str = reverse("view_and_create_transactions")

    data = {
        "name": "lala", "amount": "120.23", "amount_currency": "XYZ", "retailer": "unique_retailer", "category": "unique_category", "date": "2022-05-23", "transaction_type": "E", "recurring": "false", "user": 1,
    }
    list_response: Response = api_client.post(
        list_transaction_url, data=data, format="json"
    )
    print(list_response.json())
    final_count: int = Transaction.objects.count()
    assert list_response.status_code == status.HTTP_201_CREATED
    assert final_count == initial_count + 1




@pytest.mark.django_db
def test_post_transaction_twice(api_client, user_factory, category_factory, retailer_factory):
    initial_count: int = Transaction.objects.count()
    # let's create a category and a retailer
    user = user_factory()
    category: Category = category_factory(slug="unique_category", user=user)
    retailer: Retailer = retailer_factory(slug="unique_retailer", user=user)


    api_client.force_authenticate(user=user)
    list_transaction_url: str = reverse("view_and_create_transactions")

    data = {
        "name": "lala", "amount": "120.23", "amount_currency": "XYZ", "retailer": "unique_retailer", "category": "unique_category", "date": "2022-05-23", "transaction_type": "E", "recurring": "false", "user": 1,
    }
    list_response: Response = api_client.post(
        list_transaction_url, data=data, format="json"
    )
    # now let's post it again
    second_list_response: Response = api_client.post(
        list_transaction_url, data=data, format="json"
    ) 
    json_response: dict[str, list[str]] = second_list_response.json()
    assert "The fields name, amount, amount_currency, retailer, category, date, transaction_type, recurring, user must make a unique set." in json_response["non_field_errors"]
    final_count: int = Transaction.objects.count()
    assert second_list_response.status_code == status.HTTP_400_BAD_REQUEST
    # let's also assert that the count hasn't changed
    assert Transaction.objects.count() == final_count
