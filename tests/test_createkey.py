import pytest
import subprocess
import os

from src.createkey import generate_rsa_key

def test_openssl_rsa_key_generation():
    print("Test started: OpenSSL RSA key generation")

    if os.path.exists("private_key.pem"):
        print("Existing key file found. Removing it.")
        os.remove("private_key.pem")

    # Run the function
    generate_rsa_key()

    # Check if the key file was created
    assert os.path.exists("private_key.pem"), "private_key.pem was not created"
    print("Key file created.")

    # Check if it's not empty
    assert os.path.getsize("private_key.pem") > 0, "private_key.pem is empty"
    print("Key file is not empty.")

    # Cleanup
    os.remove("private_key.pem")
    print("Test passed and cleanup done.")