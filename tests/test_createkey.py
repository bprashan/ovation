import pytest
import subprocess
import os

def generate_rsa_key():
    command = [
        "openssl", "genrsa", 
        "-out", "private_key.pem", 
        "2048"
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)

def test_openssl_rsa_key_generation():
    # Remove the key file if it already exists
    if os.path.exists("private_key.pem"):
        os.remove("private_key.pem")

    # Run the function
    generate_rsa_key()

    # Test that the key file was created
    assert os.path.exists("private_key.pem"), "private_key.pem was not created"

    # Optional: Check if the file is not empty
    assert os.path.getsize("private_key.pem") > 0, "private_key.pem is empty"

    # Cleanup
    # os.remove("private_key.pem")

