import os

# Generate a 32-byte random secret key and convert to a hexadecimal string
secret_key = os.urandom(32).hex()
print(secret_key)
