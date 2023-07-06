from rest_framework.response import Response
from wallet_processor.models import Customer
from wallet_processor.serializers import CustomerSerializer
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class CustomerDetailView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the customer',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description='OK',
                schema=CustomerSerializer,
            ),
            404: 'Customer not found',
        }
    )
    def get(self, request, id):
        # Retrieve the customer and serialize the data
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the customer',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            204: 'Customer deleted successfully',
            404: 'Customer not found',
        }
    )
    def delete(self, request, id):
        # Delete the customer
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the customer',
                required=True,
                type=openapi.TYPE_INTEGER,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                # Add more properties as needed
            },
            required=['id'],
        ),
        responses={
            200: openapi.Response(
                description='Customer updated successfully',
                schema=CustomerSerializer,
            ),
            400: 'Invalid request payload',
            404: 'Customer not found',
        }
    )
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
