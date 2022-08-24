from django.urls import path

from expenses.api.views import (
    CategoryList,
    RetailerList,
    TransactionList,
    CategoryRUD,
    RetailerRUD,
    TransactionRUD,
)

urlpatterns = [
    path(
        "categories/",
        CategoryList.as_view(),
        name="view_and_create_categories",
    ),
    path(
        "categories/<int:pk>/",
        CategoryRUD.as_view(),
        name="retrieve_update_delete_category",
    ),
    path("retailers/", RetailerList.as_view(), name="view_and_create_retailers"),
    path(
        "retailers/<int:pk>/",
        RetailerRUD.as_view(),
        name="retrieve_update_delete_retailer",
    ),
    path(
        "transactions/", TransactionList.as_view(), name="view_and_create_transactions"
    ),
    path(
        "transactions/<int:pk>/",
        TransactionRUD.as_view(),
        name="retrieve_update_delete_transaction",
    ),
]
