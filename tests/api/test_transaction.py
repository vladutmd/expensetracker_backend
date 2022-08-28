from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Category, Retailer, Transaction


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient, transaction_factory):
    # let's create a transaction
    transaction: Transaction = transaction_factory()
    transaction_id: int = transaction.id
    get_transaction_url: str = reverse("retrieve_update_delete_transaction", args=[transaction_id])
    get_response: Response = api_client.get(
        get_transaction_url,
    )
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_own_transaction_with_token(api_client: APIClient, user_factory, transaction_factory):
    user = user_factory()
    transaction: Transaction = transaction_factory(user=user)
    transaction_id: int = transaction.id
    get_transaction_url: str = reverse("retrieve_update_delete_transaction", args=[transaction_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_transaction_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "amount": f"{transaction.amount.amount.quantize(Decimal('0.00'))}",
        "amount_currency": str(transaction.amount.currency),
        "category": transaction.category.slug,
        "date": transaction.date,
        "id": transaction.id,
        "name": transaction.name,
        "recurring": transaction.recurring,
        "retailer": transaction.retailer.slug,
        "transaction_type": transaction.transaction_type,
        "user": transaction.user.id,
    }


@pytest.mark.django_db
def test_get_someone_elses_transaction_with_token(api_client: APIClient, user_factory, transaction_factory):
    user = user_factory()
    user_2 = user_factory()
    transaction: transaction = transaction_factory(user=user_2)
    transaction_id: int = transaction.id
    get_transaction_url: str = reverse("retrieve_update_delete_transaction", args=[transaction_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_transaction_url,
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # let's now log in the client with user_2
    api_client.force_authenticate(user=user_2)
    get_response: Response = api_client.get(
        get_transaction_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "amount": f"{transaction.amount.amount.quantize(Decimal('0.00'))}",
        "amount_currency": str(transaction.amount.currency),
        "category": transaction.category.slug,
        "date": transaction.date,
        "id": transaction.id,
        "name": transaction.name,
        "recurring": transaction.recurring,
        "retailer": transaction.retailer.slug,
        "transaction_type": transaction.transaction_type,
        "user": transaction.user.id,
    }


@pytest.mark.django_db
def test_update_transaction(
    api_client: APIClient,
    user_factory,
    transaction_factory,
    category_factory,
    retailer_factory,
):
    user = user_factory()
    category: Category = category_factory(user=user)
    retailer: Retailer = retailer_factory(user=user)
    transaction: Transaction = transaction_factory(user=user, category=category, retailer=retailer, name="original_nme")
    transaction_id: int = transaction.id
    transaction_url: str = reverse("retrieve_update_delete_transaction", args=[transaction_id])
    api_client.force_authenticate(user=user)
    print(transaction.category.__dict__)
    print(transaction.retailer.__dict__)
    response: Response = api_client.put(
        transaction_url,
        data={
            "amount": f"{transaction.amount.amount.quantize(Decimal('0.00'))}",
            "amount_currency": str(transaction.amount.currency),
            "category": transaction.category.slug,
            "date": transaction.date,
            "id": transaction.id,
            "name": "new_name",
            "recurring": transaction.recurring,
            "retailer": transaction.retailer.slug,
            "transaction_type": "E",
            "user": transaction.user.id,
        },
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    transaction.refresh_from_db()
    assert transaction.name == "new_name"

    # let's create a new user and see if we can change the user of this transaction
    user_2 = user_factory()
    response: Response = api_client.put(
        transaction_url,
        data={
            "amount": f"{transaction.amount.amount.quantize(Decimal('0.00'))}",
            "amount_currency": str(transaction.amount.currency),
            "category": transaction.category.slug,
            "date": transaction.date,
            "id": transaction.id,
            "name": "new_name",
            "recurring": transaction.recurring,
            "retailer": transaction.retailer.slug,
            "transaction_type": "E",
            "user": user_2.id,
        },
    )
    transaction.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert transaction.user == user
    # good, it did not change


@pytest.mark.django_db
def test_delete_transaction(api_client: APIClient, user_factory, transaction_factory):
    user = user_factory()
    transaction: Transaction = transaction_factory(user=user, name="gonna_have_to_go")
    transaction_id: int = transaction.id
    transaction_url: str = reverse("retrieve_update_delete_transaction", args=[transaction_id])
    api_client.force_authenticate(user=user)
    response: Response = api_client.delete(transaction_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Transaction.DoesNotExist):
        Transaction.objects.get(id=transaction_id)
