# Wallet App

The Wallet App is a Django-based application that handles transaction processing and balance management for customers.

## Prerequisites

Before setting up the Wallet App, make sure you have the following prerequisites installed on your system:

- Python (version X.X.X)
- Django (version X.X.X)
- Django REST Framework (version X.X.X)

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

 

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).