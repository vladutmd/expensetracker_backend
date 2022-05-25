from django.urls import path

from expenses.api.views import CategoryList, RetailerList, TransactionList

urlpatterns = [
    path(
        "categories/",
        CategoryList.as_view(),
        name="view_and_create_categories",
    ),
    path("retailers/", RetailerList.as_view(), name="view_and_create_retailers"),
    path("transactions/", TransactionList.as_view(), name="view_and_create_transactions"),
]
