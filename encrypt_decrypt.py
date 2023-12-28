from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


import os

"""
Work-Flow
1 -> read raw bytes of a file
2 -> generate a key
3 -> encrypt those using the generated key
4 -> decrypt those using the generate key
5 -> write those into a file
"""

def encrypt(data, key):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    
    # Create a cipher object with AES algorithm, CBC mode, and the provided key
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Apply padding to the data before encryption
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the IV and ciphertext
    return iv + ciphertext

def decrypt(encrypted_data, key):
    # Extract the IV from the encrypted data
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    # Create a cipher object with AES algorithm, CBC mode, and the provided key
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding after decryption
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(decrypted_data) + unpadder.finalize()

    return data

def generateKey() -> bytes:
    return os.urandom(32)


if __name__ == "__main__":
    # Generate a random key (make sure to keep it secret and secure)
    key = os.urandom(32)

    # Original data
    with open("files_uploaded/Nqueens.txt", "rb") as jammer:
        original_data = jammer.read()
    # original_data = b"Hello, this is a secret message!"

    # Encrypt the data
    encrypted_data = encrypt(original_data, key)
    
    # Decrypt the data
    decrypted_data = decrypt(encrypted_data, key)
        
    print(key)
    # Check if the decrypted data matches the original data
    print(type(original_data))  # This should be True