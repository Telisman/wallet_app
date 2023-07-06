from rest_framework.response import Response
from wallet_processor.models import Customer
from wallet_processor.serializers import CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView

class CustomerDetailView(APIView):
    def get(self, request, id):
        # Retrieve the customer and serialize the data
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, id):
        # Delete the customer
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        # Update the customer
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)