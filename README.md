# Wallet App

The Wallet App is a Django-based application that handles transaction processing and balance management for customers.

## Prerequisites

Before setting up the Wallet App, make sure you have the following prerequisites installed on your system:

- Python (version 3.10.5)
- Django (version 4.2.2)
- Django REST Framework (version 3.14.0)

## Installation

1. Clone the repository:

git clone https://github.com/your-username/wallet-app.git


2. Navigate to the project directory:
cd wallet-app


3. Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate



4. Install the project dependencies:

pip install -r requirements.txt



5. Configure are Setting and create connection with PostgresSQL:


```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<name_of_your_database>',
        'USER': '< user >',
        'PASSWORD': '< your_password >',
        'HOST': '< your_host >',
        'PORT': '< your_port >',
    }
}
```
You can use given default setings: in settings.py

6. Run database migrations:

create superuser for are project


7. Run database migrations:

python manage.py migrate

8. Add Customer manually:

After adding a customer or multiple customers, an API key will appear in the database for each new customer entered

## Usage

1. Start the development server:

python manage.py runserver



2. Access the API endpoints:

- Customers: `http://localhost:8000/customers/:<id>`
Will display only first and last name of Customer, selected by id


- Transactions: `http://localhost:8000/transactions/` - you need to use api key for transactions: 
Generated API key: 2a255cd495cfb37a610747f42c5f2dc616f5178e20d6aa33b5d30f6d73cc1497


- Customers: `http://localhost:8000/customers/:<id>/?api_key=<customers_api_key>`
Will display only first and last name and balance from Customer, selected by id and his api_key


3. Make requests to the API using a tool like Postman or cURL.

4. Use the available endpoints to perform various operations such as creating customers, processing transactions, and retrieving customer information.

## Configuration

The Wallet App can be configured through the following environment variables:

- `DATABASE_URL`: The URL of the database to be used (e.g., `postgres://user:password@localhost:5432/wallet_app`)
- `SECRET_KEY`: The secret key used by Django for cryptographic signing and security purposes
- `API_KEY`: The API key required to access protected endpoints

 

## Extra links

https://documenter.getpostman.com/view/28385092/2s93zFYKfu

## Functionality

Function, split_transactions, takes a list of transactions as input and splits them into chunks based on their priority. 
```
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
            total_value = sum(t['value'] for t in current_chunk)
            print("Chunk {}:".format(len(chunks)))
            print("\ttransaction: {}".format(current_chunk))
            print("\ttotal value: {}".format(total_value))
            print("\ttime left: {}\n".format(remaining_time))
            current_chunk = [transaction]
            remaining_time = 1000 - transaction['latency']  
```

Function, send_to_wallet_processor, is responsible for sending a chunk of transactions to a wallet processor for further processing. 


```


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


```

 function, execute_transaction, is responsible for executing a single transaction for a customer
 
```

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



```

 function, process_transactions, is an API view function designed to handle a POST request for processing transactions. Here's a breakdown of how the function works
 


```
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
```


code snippet provided extends the CustomerDetailView class with two additional methods: delete and patch. These methods handle the HTTP DELETE and PATCH methods, respectively, for deleting and updating a specific customer.

```
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

``` 


code snippet provided represents the get method inside a class-based view. This method is responsible for retrieving details of a specific customer identified by id


``` 
  def get(self, request, id):
        # Retrieve the customer and serialize the data
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)
``` 