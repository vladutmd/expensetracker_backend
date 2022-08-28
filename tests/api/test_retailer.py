import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from expenses.models import Retailer


@pytest.mark.django_db
def test_authentication_required(api_client: APIClient, retailer_factory):
    # let's create a retailer
    retailer: Retailer = retailer_factory()
    retailer_id: int = retailer.id
    get_retailer_url: str = reverse("retrieve_update_delete_retailer", args=[retailer_id])
    get_response: Response = api_client.get(
        get_retailer_url,
    )
    assert get_response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_own_retailer_with_token(api_client: APIClient, user_factory, retailer_factory):
    user = user_factory()
    retailer: retailer = retailer_factory(user=user)
    retailer_id: int = retailer.id
    get_retailer_url: str = reverse("retrieve_update_delete_retailer", args=[retailer_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_retailer_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "id": retailer_id,
        "name": retailer.name,
        "online": retailer.online,
        "user": user.id,
        "slug": retailer.slug,
    }


@pytest.mark.django_db
def test_get_someone_elses_retailer_with_token(api_client: APIClient, user_factory, retailer_factory):
    user = user_factory()
    user_2 = user_factory()
    retailer: retailer = retailer_factory(user=user_2)
    retailer_id: int = retailer.id
    get_retailer_url: str = reverse("retrieve_update_delete_retailer", args=[retailer_id])
    api_client.force_authenticate(user=user)
    get_response: Response = api_client.get(
        get_retailer_url,
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

    # let's now log in the client with user_2
    api_client.force_authenticate(user=user_2)
    get_response: Response = api_client.get(
        get_retailer_url,
    )
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json() == {
        "id": retailer_id,
        "name": retailer.name,
        "online": retailer.online,
        "user": user_2.id,
        "slug": retailer.slug,
    }


@pytest.mark.django_db
def test_update_retailer(api_client: APIClient, user_factory, retailer_factory):
    user = user_factory()
    retailer: retailer = retailer_factory(user=user, name="original_nme")
    retailer_id: int = retailer.id
    retailer_url: str = reverse("retrieve_update_delete_retailer", args=[retailer_id])
    api_client.force_authenticate(user=user)
    response: Response = api_client.put(
        retailer_url,
        data={"name": "new_name", "online": retailer.online, "slug": retailer.slug},
    )
    assert response.status_code == status.HTTP_200_OK
    retailer.refresh_from_db()
    assert retailer.name == "new_name"

    # let's create a new user and see if we can change the user of this retailer
    user_2 = user_factory()
    response: Response = api_client.put(
        retailer_url,
        data={
            "name": retailer.name,
            "online": retailer.online,
            "user": user_2.id,
            "slug": retailer.slug,
        },
    )
    retailer.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert retailer.user == user
    # good, it did not change


@pytest.mark.django_db
def test_delete_retailer(api_client: APIClient, user_factory, retailer_factory):
    user = user_factory()
    retailer: retailer = retailer_factory(user=user, name="gonna_have_to_go")
    retailer_id: int = retailer.id
    retailer_url: str = reverse("retrieve_update_delete_retailer", args=[retailer_id])
    api_client.force_authenticate(user=user)
    response: Response = api_client.delete(retailer_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    with pytest.raises(Retailer.DoesNotExist):
        Retailer.objects.get(id=retailer_id)
