from django.urls import path
from .views import (
 UserRegister, UserLogin,
   UserLogout, UserView,
   BalanceCheckView, BalanceTransferView,
   TransactionHistoryView)

urlpatterns = [
     path('register/', UserRegister.as_view(), name='register' ),
     path('login/', UserLogin.as_view(), name='login'),
     path('logout/', UserLogout.as_view(), name='logout'),
     path('user/', UserView.as_view(), name='user'),
     path('balance-check/', BalanceCheckView.as_view(), name='balance_check'),
     path('balance-transfer/', BalanceTransferView.as_view(), name='balance-transfer'),
     path('transaction-history/', TransactionHistoryView.as_view(), name='transaction-history'),
]