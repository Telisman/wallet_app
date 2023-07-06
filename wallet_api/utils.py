import requests
from wallet_processor.views import execute_transaction
from wallet_processor.models import Customer

def split_transactions(transactions):
    # Sort transactions by priority (value and latency)
    sorted_transactions = sorted(transactions, key=lambda t: (t['value'], -t['latency']), reverse=True)

    # Split transactions into chunks
    chunks = []
    current_chunk = []
    remaining_time = 1000

    for transaction in sorted_transactions:
        if transaction['latency'] <= remaining_time:
            current_chunk.append(transaction)
            remaining_time -= transaction['latency']
        else:
            chunks.append(current_chunk)
            current_chunk = [transaction]
            remaining_time = 1000 - transaction['latency']

    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def send_to_wallet_processor(chunk):
    endpoint = 'http://127.0.0.1:8000/transaction/'  # Update the endpoint URL with the correct URL

    # Prepare the payload
    payload = {'chunk': chunk}

    # Send the HTTP POST request to the wallet-processor
    response = requests.post(endpoint, json=payload)

    # Check the response status
    if response.status_code == 200:
        # Transactions sent to the wallet-processor successfully
        transactions = response.json().get('transactions')
        for transaction in transactions:
            execute_transaction(transaction)  # Execute the transaction logic
        print('Chunk processed successfully.')
    else:
        print('Failed to process chunk.')

def execute_transaction(transaction):
    customer_id = transaction['customer']
    value = transaction['value']

    # Retrieve the customer from the database
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        print(f"Customer with ID {customer_id} does not exist.")
        return

    # Check if the customer has sufficient balance
    if customer.balance >= value:
        # Update the customer's balance
        customer.balance -= value
        customer.save()
        # Execute additional transaction logic if needed

        # Log the successful transaction
        print(f"Transaction executed for Customer {customer_id}. Remaining balance: {customer.balance}")
    else:
        # Log the insufficient balance and handle the transaction failure
        print(f"Transaction failed for Customer {customer_id}. Insufficient balance: {customer.balance}")
