import subprocess
import os

def generate_rsa_key():
    command = [
        "openssl", "genrsa",
        "-out", "private_key.pem",
        "2048"
    ]

    print("Starting RSA key generation using OpenSSL...")

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("RSA key generated successfully: private_key.pem")
    except subprocess.CalledProcessError as e:
        print(f"OpenSSL command failed: {e.stderr}")
        raise