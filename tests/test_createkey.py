import pytest
import subprocess
import os
import logging

from src.createkey import generate_rsa_key

def test_openssl_rsa_key_generation():
    logging.info("Test started: OpenSSL RSA key generation")

    if os.path.exists("private_key.pem"):
        logging.info("Existing key file found. Removing it.")
        os.remove("private_key.pem")

    # Run the function
    generate_rsa_key()

    # Check if the key file was created
    assert os.path.exists("private_key.pem"), "private_key.pem was not created"
    logging.info("Key file created.")

    # Check if it's not empty
    assert os.path.getsize("private_key.pem") > 0, "private_key.pem is empty"
    logging.info("Key file is not empty.")

    # Cleanup
    os.remove("private_key.pem")
    logging.info("Test passed and cleanup done.")

