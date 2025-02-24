from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/', AccountListCreateView.as_view(), name='accounts'),
    path('transactions/', TransactionListCreateView.as_view(), name='transactions'),
    path('accounts/<int:pk>/', AccountRetrieveUpdateDestroyView.as_view(), name='account-detail'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
    path('stats/', TransactionStatsView.as_view(), name='transaction-stats'),
]
