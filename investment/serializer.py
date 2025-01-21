from rest_framework import serializers
from .models import InvestmentPlan

class InvestmentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPlan
        fields = '__all__'
