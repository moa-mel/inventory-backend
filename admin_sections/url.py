from django.urls import path

from admin_sections.views import RetrievePendingTransactionView, CreateInvestmentView, AdminRetrieveInvestmentView, UpdateInvestmentView, DeleteInvestmentView, TransactionStatusView, AdminLoginView

urlpatterns = [
     
     path(
        "login/",
        AdminLoginView.as_view(),
        name="admin-login",
    ),
    # GET /transactions/ - View all pending transactions (Admin-only).
    path(  
        "transactions/pending/",
        RetrievePendingTransactionView.as_view(),
        name="retrieve-pending-transaction",
    ),
    # PUT /transactions/:id/ - Approve/reject a transaction (Admin-only).
    path(  
        "transactions/<str:id>/",
        TransactionStatusView.as_view(),
        name="approve-reject-transaction",
    ),
    # POST /investment-plans/ - Add a plan (Admin-only)
    path(
        "create/investment/",
        CreateInvestmentView.as_view(),
        name="create-investment",
    ),
    # GET /investment-plans/ - View all plans (Investors/Admins).
    path(
        "investment/",
        AdminRetrieveInvestmentView.as_view(),
        name="Admin-Retrieve-investment",
    ),
    # PUT /investment-plans/:id/ - Update a plan (Admin-only)
    path(
        "edit/investment/<str:id>/",
        UpdateInvestmentView.as_view(),
        name="Edit-investment",
    ),
    # DELETE /investment-plans/:id/ - Delete a plan (Admin-only)
    path(
        "delete/investment/<str:id>/",
        DeleteInvestmentView.as_view(),
        name="Delete-investment",
    ),
]