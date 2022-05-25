from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from expenses.api.serializers import CategorySerializer, RetailerSerializer, TransactionSerializer
from expenses.models import Category, Retailer, Transaction


class CategoryList(generics.ListCreateAPIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        This ensures only the categories created by the user are returned.
        """
        user = self.request.user
        return Category.objects.filter(user=user)

    def perform_create(self, serializer):
        print(serializer.__dict__)
        serializer.save(user=self.request.user)


class RetailerList(generics.ListCreateAPIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RetailerSerializer

    def get_queryset(self):
        """
        This ensures only the retailers created by the user are returned.
        """
        user = self.request.user
        return Retailer.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionList(generics.ListCreateAPIView):
    authentication_classes = [JWTCookieAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """
        This ensures only the retailers created by the user are returned.
        """
        user = self.request.user
        return Transaction.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)