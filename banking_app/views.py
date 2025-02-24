from django.shortcuts import render
from rest_framework import generics
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

# AccountListCreate View from here
class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# TransactionListCreate View from here
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.user != self.request.user:
            raise PermissionDenied("You do not own this account.")
        serializer.save(user=self.request.user)

# AccountRetrieveUpdateDestroy View from here, to enable patch, put and delete
class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

# TransactionRetrieveUpdateDestroy View from here, to enable patch, put and delete
class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

# TransactionStats View from here to get the data for graphs and charts
class TransactionStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        Returns a list of transactions filtered by query parameters.
        Frontend can use this data to create charts, tables, etc.
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        category = request.query_params.get('category')
        transaction_type = request.query_params.get('type')
        account_id = request.query_params.get('account')  # New filter for account

        # Base queryset: Filter transactions for the authenticated user
        transactions = Transaction.objects.filter(user=request.user)
        
        # Apply filters by date range, category, transaction type (credit/debit), and account
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])
        if category:
            transactions = transactions.filter(category=category)
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)
        if account_id:
            transactions = transactions.filter(account_id=account_id)

        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'transactions': serializer.data,
            'filters': {
                'start_date': start_date,
                'end_date': end_date,
                'category': category,
                'type': transaction_type,
                'account': account_id
            }
        })
