from uuid import uuid4
from django.db import models

from user.models import User

# Create your models here.
class InvestmentPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    minimum_investment = models.PositiveIntegerField(default=0)
    subscribers = models.ManyToManyField(User, related_name="investment_plans", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
