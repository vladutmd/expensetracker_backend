from django.urls import path

from expenses.api.views import CategoryList, RetailerList

urlpatterns = [
    path(
        "categories/",
        CategoryList.as_view(),
        name="view_and_create_categories",
    ),
    path("retailers/", RetailerList.as_view(), name="view_and_create_retailers"),
]
