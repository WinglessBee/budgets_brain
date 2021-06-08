from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from brain.budgets import models
from brain.budgets import serializers


class ProfileView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return models.Profile.objects.filter(user=self.request.user)


class AccountView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        return models.Account.objects.filter(user=self.request.user)


class BudgetView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BudgetSerializer

    def get_queryset(self):
        return models.Budget.objects.filter(user=self.request.user)


class IncomeView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.IncomeSerializer

    def get_queryset(self):
        return models.Income.objects.select_related('activity').filter(activity__user=self.request.user)


class ExpenseView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ExpenseSerializer

    def get_queryset(self):
        return models.Expense.objects.select_related('activity').filter(activity__user=self.request.user)


class TransferView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TransferSerializer

    def get_queryset(self):
        return models.Transfer.objects.select_related('activity').filter(activity__user=self.request.user)
