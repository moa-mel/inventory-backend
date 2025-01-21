from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from user.permissions import IsInvestor
from .models import InvestmentPlan
from .serializer import InvestmentPlanSerializer
from rest_framework.views import APIView

class RetrieveInvestmentView(APIView):
    """
    Retrieve all investment plans. Admins and Investors can view plans.
    """
    permission_classes = [IsAuthenticated, IsInvestor]

    def get(self, request):
        plans = InvestmentPlan.objects.all()
        serializer = InvestmentPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvestmentSubscribeView(APIView):
    """
    Subscribe to an investment plan by its ID. Only investors can subscribe.
    """
    permission_classes = [IsAuthenticated, IsInvestor]

    def post(self, request, id):
        try:
            # Check if the plan exists
            plan = InvestmentPlan.objects.get(id=id)
        except InvestmentPlan.DoesNotExist:
            return Response(
                {"error": "Investment plan not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Perform the subscription logic (e.g., create a record in a subscription model)
        # For simplicity, assuming a 'subscribers' many-to-many relationship exists
        user = request.user
        if user in plan.subscribers.all():
            return Response(
                {"error": "You have already subscribed to this plan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan.subscribers.add(user)  # Add the user to the plan's subscribers
        return Response(
            {"message": f"You have successfully subscribed to {plan.name}."},
            status=status.HTTP_200_OK,
        )