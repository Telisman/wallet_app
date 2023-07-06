from django.urls import path
from wallet_api.views import CustomerDetailView

app_name = 'wallet_api'

urlpatterns = [
    path('customer/:<int:id>/', CustomerDetailView.as_view(), name='customer_detail'),
]