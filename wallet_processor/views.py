from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from wallet_processor.utils import execute_transaction
from wallet_api.utils import split_transactions



@api_view(['POST'])
@csrf_exempt
def process_transactions(request):
    if request.method == 'POST':
        try:
            transactions = request.data  # Access the JSON payload directly

            if transactions:
                # Split transactions into chunks
                chunks = split_transactions(transactions)

                # Process chunks
                for chunk in chunks:
                    for transaction in chunk:
                        execute_transaction(transaction)

                return Response({'message': 'Transactions processed successfully.'})
            else:
                return Response({'error': 'No transactions provided.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
