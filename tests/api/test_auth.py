from typing import Dict
import pytest
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


@pytest.mark.django_db
def test_registration_verification_and_authentication(api_client):
    current_user_count: int = User.objects.all().count()
    current_mail_count: int = len(mail.outbox)

    email: str = "suchgoodemail@aws.moon"
    password: str = "amazingpassword"
    registration_data: Dict[str, str] = {
        "email": email,
        "password1": password,
        "password2": password,
    }

    register_url: str = reverse("rest_register")
    response: Response = api_client.post(register_url, data=registration_data)
    # check that the user was created successfully
    assert response.status_code == status.HTTP_201_CREATED
    # check that the user count increased by one
    assert User.objects.all().count() == (current_user_count + 1)
    assert len(mail.outbox) == (current_mail_count + 1)
    assert "key" not in response.data

    # if we try to log in without verifying should get HTTP 400
    login_url: str = reverse("rest_login")
    login_response: Response = api_client.post(
        login_url,
        data={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == status.HTTP_400_BAD_REQUEST

    # let's verify the user
    # TODO: rewrite the part below. is there another way to get the key?
    verify_url: str = reverse("rest_verify_email")
    key: str = mail.outbox[-1].body.split("/")[-2]
    verify_response: Response = api_client.post(verify_url, data={"key": key})
    assert verify_response.status_code == status.HTTP_200_OK

    # now let's try logging in again
    login_response: Response = api_client.post(
        login_url,
        data={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == status.HTTP_200_OK

    # check if we got an access token
    assert "access_token" in login_response.data


@pytest.mark.django_db
def test_authentication_with_verified_email(api_client, user_factory):
    email = "bad@email.com"
    password = "amazingsecurity"
    _ = user_factory(email=email, password=password)
    login_url: str = reverse("rest_login")
    login_response: Response = api_client.post(
        login_url,
        data={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_registration_verification_and_authentication_with_get_endpoint(api_client):
    current_user_count: int = User.objects.all().count()
    current_mail_count: int = len(mail.outbox)

    email: str = "suchgoodemail2@aws.moon"
    password: str = "amazingpassword2"
    registration_data: Dict[str, str] = {
        "email": email,
        "password1": password,
        "password2": password,
    }

    register_url: str = reverse("rest_register")
    response: Response = api_client.post(register_url, data=registration_data)
    # check that the user was created successfully
    assert response.status_code == status.HTTP_201_CREATED
    # check that the user count increased by one
    assert User.objects.all().count() == (current_user_count + 1)
    assert len(mail.outbox) == (current_mail_count + 1)
    assert "key" not in response.data

    # if we try to log in without verifying should get HTTP 400
    login_url: str = reverse("rest_login")
    login_response: Response = api_client.post(
        login_url,
        data={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == status.HTTP_400_BAD_REQUEST

    email_body: str = mail.outbox[-1].body
    start_of_link: int = email_body.find(
        "http"
    )  # not adding more in case we want to later add https
    link: str = email_body[start_of_link:].split("\n")[0]
    # now let's GET request that and we should have been redirected
    response: Response = api_client.get(link)
    assert response.status_code == 302

    redirect_url: str = response.url
    assert (redirect_url + "/").endswith(login_url)

    # now let's try logging in again
    login_response: Response = api_client.post(
        login_url,
        data={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == status.HTTP_200_OK

    # check if we got an access token
    assert "access_token" in login_response.data
