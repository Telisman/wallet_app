from rest_framework import serializers
from .models import Customer, APIKey

class CustomerSerializer(serializers.ModelSerializer):

    balance = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'balance']

    def get_balance(self, obj):
        request = self.context.get('request')
        api_key = request.query_params.get('api_key')

        try:
            api_key_obj = APIKey.objects.get(key=api_key)
            if api_key_obj.customer == obj:
                return obj.balance
        except APIKey.DoesNotExist:
            pass

        return None



