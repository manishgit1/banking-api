from django.urls import path
from .views import (
   BalanceCheckView, BalanceTransferView,
   TransactionHistoryView, TransactionSummary)

urlpatterns = [
     path('balance-check', BalanceCheckView.as_view(), name='balance_check'),
     path('balance-transfer', BalanceTransferView.as_view(), name='balance-transfer'),
     path('transaction-history', TransactionHistoryView.as_view(), name='transactions-history'),
     path('transaction-summary', TransactionSummary.as_view(), name='transactions-summary'),
   #  path('transaction-category', TransactionByCategory.as_view(), name='transactions-category'),
]
