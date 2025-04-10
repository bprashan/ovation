import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(message, host='127.0.0.1', port=65432):
    logging.info(f"Connecting to server at {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        logging.info(f"Sending message: {message}")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        logging.info(f"Received response: {data.decode()}")
        return data.decode()

