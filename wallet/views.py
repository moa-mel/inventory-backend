from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsRegularUser
from .models import Wallet, Transaction
from .serializer import WalletSerializer
from rest_framework import status
from django.db import transaction

class WalletView(APIView):
    """
    Retrieve the wallet balance and transaction history for the authenticated user.
    """
    permission_classes = [IsAuthenticated, IsRegularUser]

    def get(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
            serializer = WalletSerializer(wallet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)


class DepositView(APIView):
    permission_classes = [IsAuthenticated, IsRegularUser]

    def post(self, request):
        try:
            wallet, created = Wallet.objects.get_or_create(user=request.user)

            amount = request.data.get('amount')
            if not amount or float(amount) <= 0:
                return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

            transaction = Transaction.objects.create(
                wallet=wallet,  # Ensure this matches your model definition
                type="Deposit",
                amount=amount,
                user=request.user,
                status="Pending"
            )
            return Response(
                {
                    "message": "Deposit request submitted. Awaiting approval.",
                    "transaction_id": transaction.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WithdrawWalletView(APIView):
    """
    Create a withdrawal request for the authenticated user's wallet.
    """
    permission_classes = [IsAuthenticated, IsRegularUser]

    def post(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
            amount = request.data.get('amount')

            if not amount or float(amount) <= 0:
                return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

            if float(amount) > wallet.balance:
                return Response(
                    {"error": "Insufficient wallet balance."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            transaction = Transaction.objects.create(
                wallet=wallet,
                type="Withdraw",
                amount=amount,
                status="Pending"
            )

            # Deduct the balance temporarily, awaiting approval
            wallet.balance -= float(amount)
            wallet.save()

            return Response(
                {
                    "message": "Withdrawal request submitted. Awaiting approval.",
                    "transaction_id": transaction.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)