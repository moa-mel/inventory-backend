from uuid import uuid4
from django.db import models

from user.models import User

TRANSACTION_TYPES = [
    ('DEPOSIT', 'DEPOSIT'), 
    ('WITHDRAW', 'WITHDRAW'),
]
TRANSACTION_STATUSES = [
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
]

# Create your models here.
class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField(default=0)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUSES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
