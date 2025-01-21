from django.urls import path

from investment.views import RetrieveInvestmentView, InvestmentSubscribeView

urlpatterns = [
    # GET /investment-plans/ - View all plans (Admins)
    path(
        "investment-plans/",
        RetrieveInvestmentView.as_view(),
        name="retrieve-investment",
    ),
    # POST /subscribe/:id/ - Investors can subscribe to a plan.
   path(
        "subscribe/<str:id>/",
        InvestmentSubscribeView.as_view(),
        name="investment-subscribe",
    ),
]