from wallet_processor.models import Customer

def execute_transaction(transaction):
    customer_id = transaction['customer_id']
    value = transaction['value']

    # Retrieve the customer from the database
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        print(f"Customer with ID {customer_id} does not exist.")
        return

    # Check if the customer has sufficient balance
    if customer.balance >= value:
        # Update the customer's balance
        customer.balance -= value
        customer.save()

        # Log the successful transaction
        print(f"Transaction executed for Customer {customer_id}. Remaining balance: {customer.balance}")
    else:
        # Log the insufficient balance and handle the transaction failure
        print(f"Transaction failed for Customer {customer_id}. Insufficient balance: {customer.balance}")
