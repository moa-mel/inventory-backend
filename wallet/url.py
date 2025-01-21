from django.urls import path

from wallet.views import DepositView, WalletView, WithdrawWalletView


urlpatterns = [
    # View wallet balance and transaction history - GET
    path( 
        "retrieve-wallet/",
        WalletView.as_view(),
        name="Wallet",
    ),
    # Create a deposit request - POST
    path(
        "create/wallet-deposit/",
        DepositView.as_view(),
        name="deposit-wallet",
    ),
    # Create a withdrawal request - POST
    path(
        "create/wallet-withdraw/",
        WithdrawWalletView.as_view(),
        name="withdraw-wallet",
    ),
]