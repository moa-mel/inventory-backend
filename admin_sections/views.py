from django.shortcuts import render
from rest_framework.views import APIView
from investment.models import InvestmentPlan
from investment.serializer import InvestmentPlanSerializer
from user.models import User
from user.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from wallet.models import Transaction
from wallet.serializer import TransactionSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




class AdminLoginView(APIView):
    def post(self, request):
        """
        Log in an admin user. Requires 'username' and 'password'.
        Returns access and refresh tokens if login is successful.
        """
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if user is None or not user.is_staff:
            return Response(
                {"error": "Invalid credentials or you do not have admin privileges."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class RetrievePendingTransactionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        transactions = Transaction.objects.filter(status="pending")
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransactionStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, id):
        try:
            transaction = Transaction.objects.get(id=id)
            transaction.status = request.data.get("status", transaction.status)
            transaction.save()
            return Response({"message": "Transaction status updated successfully."}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateInvestmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = InvestmentPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminRetrieveInvestmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        plans = InvestmentPlan.objects.all()
        serializer = InvestmentPlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateInvestmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, id):
        try:
            plan = InvestmentPlan.objects.get(id=id)
            serializer = InvestmentPlanSerializer(plan, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestmentPlan.DoesNotExist:
            return Response({"error": "Investment plan not found."}, status=status.HTTP_404_NOT_FOUND)


class DeleteInvestmentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, id):
        try:
            plan = InvestmentPlan.objects.get(id=id)
            plan.delete()
            return Response({"message": "Investment plan deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except InvestmentPlan.DoesNotExist:
            return Response({"error": "Investment plan not found."}, status=status.HTTP_404_NOT_FOUND) 
