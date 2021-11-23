from datetime import date

import factory
from django.contrib.auth import get_user_model
from djmoney.money import Money
from expenses.models import Category, Retailer, Transaction
from allauth.account.models import EmailAddress

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", f"{email}_password")
    is_active = True
    is_staff = False

    @factory.post_generation
    def verify(obj, create, extracted, **kwargs):
        if not create:
            return
        EmailAddress.objects.create(
            email=obj.email, verified=True, primary=True, user=obj
        )


class RetailerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Retailer

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"AmazI{n}")
    online = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Category_{n}")
    product_type = "P"


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    # need to inject the same user for category and retailer
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    retailer = factory.SubFactory(RetailerFactory)
    amount = Money(420.00, "GBP")
    name = factory.Sequence(lambda n: f"Transaction_{n}")
    date = factory.Faker("date", end_datetime=date.today())
    transaction_type = "E"
    recurring = False
