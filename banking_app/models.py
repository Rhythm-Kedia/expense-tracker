from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

# Account Model to store user accounts, I'm not sure about name or number, maybe only one is required
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.account_number})"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [('credit', 'Credit'),('debit', 'Debit')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=6, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def clean(self):
        # Validate account ownership
        if self.account.user != self.user:
            raise ValidationError("You do not own this account.")
        # Validate balance for debit transactions
        if self.type == 'debit' and self.amount > self.account.balance:
            raise ValidationError("Insufficient balance.")

    def save(self, *args, **kwargs):
        self.clean()
        if not self._state.adding:
            # Fetch the original transaction from the database
            original = Transaction.objects.get(pk=self.pk)
            if original.type == 'credit':
                original.account.balance -= original.amount
            else:
                original.account.balance += original.amount

            self.account.balance = original.account.balance
            if self.amount > self.account.balance:
                raise ValidationError("Insufficient balance.")
            original.account.save()

        elif not self.date:
            self.date = timezone.now().date()
        
        if self.type == 'credit':
            self.account.balance += self.amount
        else:
            self.account.balance -= self.amount
        self.account.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Revert the transaction's impact on the account balance
        if self.type == 'credit':
            self.account.balance -= self.amount
        else:
            self.account.balance += self.amount
        self.account.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.amount} - {self.type})"