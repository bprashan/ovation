import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_server(host='127.0.0.1', port=65432):
    logging.info(f"Starting server on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        logging.info("Server is listening for incoming connections")
        conn, addr = server_socket.accept()
        with conn:
            logging.info(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    logging.info("No data received. Closing connection.")
                    break
                logging.info(f"Received data: {data.decode()}")
                conn.sendall(data)
                logging.info("Sent data back to client")

