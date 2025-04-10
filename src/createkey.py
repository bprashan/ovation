import subprocess
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def generate_rsa_key():
    command = [
        "openssl", "genrsa",
        "-out", "private_key.pem",
        "2048"
    ]

    logging.info("Starting RSA key generation using OpenSSL...")
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("RSA key generated successfully: private_key.pem")
    except subprocess.CalledProcessError as e:
        logging.error(f"OpenSSL command failed: {e.stderr}")
        raise

