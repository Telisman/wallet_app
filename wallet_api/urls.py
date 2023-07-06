from django.urls import path
from wallet_api.views import CustomerDetailView
from wallet_processor.views import process_transactions

app_name = 'wallet_api'

urlpatterns = [
    path('transaction/', process_transactions, name='process_transactions'),
    path('customer/:<int:id>/', CustomerDetailView.as_view(), name='customer_detail'),
]