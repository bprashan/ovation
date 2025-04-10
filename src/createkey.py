import subprocess

# Define the OpenSSL command
command = [
    "openssl", "genrsa", 
    "-out", "private_key.pem", 
    "2048"
]

try:
    # Execute the command
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    print("OpenSSL command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e.stderr}")

