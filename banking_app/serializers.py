from rest_framework import serializers
from .models import Account, Transaction
from django.utils import timezone

# Account Serializer to serialize account data
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'account_number', 'balance']
        read_only_fields = ['id']

# Trransaction Serializer to serialize transaction data
class TransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%Y-%m-%d", required=False)
    class Meta:
        model = Transaction
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
    def validate_account(self, value):
        # Ensure the account belongs to the authenticated user
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("You do not own this account.")
        return value
    
    def validate_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Transaction date cannot be in the future.")
        return value
    
    def to_representation(self, instance):
        """Ensure date is always returned in YYYY-MM-DD format"""
        representation = super().to_representation(instance)
        representation['date'] = instance.date.strftime("%Y-%m-%d") if instance.date else None
        return representation