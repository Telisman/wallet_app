from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from wallet_processor.utils import execute_transaction
from wallet_api.utils import split_transactions

from .api_key_generator import generate_api_key
api_value = 'your_desired_value'
api_key = generate_api_key(api_value)
print("Generated API key:", api_key)


@api_view(['POST'])
@csrf_exempt
def process_transactions(request):
    if request.method == 'POST':
        try:
            api_key = request.META.get('HTTP_AUTHORIZATION')  # Get the API key from the request headers

            generated_api_key = generate_api_key('your_desired_value')  # Generate the API key

            if api_key == generated_api_key:  # Compare with the generated API key
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
            else:
                return Response({'error': 'Invalid API key.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)