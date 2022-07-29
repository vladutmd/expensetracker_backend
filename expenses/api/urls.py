from django.urls import path

from expenses.api.views import CategoryList, RetailerList, TransactionList, CategoryRUD

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
    path("transactions/", TransactionList.as_view(), name="view_and_create_transactions"),
]
