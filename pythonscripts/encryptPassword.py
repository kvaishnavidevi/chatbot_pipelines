from cryptography.fernet import Fernet

# Generate a key (store it securely and use it for decryption)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt password
plain_password = "db_password"
encrypted_password = cipher_suite.encrypt(plain_password.encode())

print("Encryption Key:", key.decode())  # Save this key securely
print("Encrypted Password:", encrypted_password.decode())  # Store in config