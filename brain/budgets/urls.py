from django.urls import path

from brain.budgets import views


urlpatterns = [
    path('profiles', views.ProfileView.as_view()),
    path('accounts', views.AccountView.as_view()),
    path('budgets', views.BudgetView.as_view()),
    path('incomes', views.IncomeView.as_view()),
    path('expenses', views.ExpenseView.as_view()),
    path('transfers', views.TransferView.as_view()),
]
