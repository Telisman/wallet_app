import hashlib

def generate_api_key(api_value):
    # Generate an API key based on the provided value
    hashed_value = hashlib.sha256(api_value.encode()).hexdigest()
    return hashed_value
