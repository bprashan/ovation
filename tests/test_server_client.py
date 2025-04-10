import pytest
import logging
import threading
import time
from src.server import start_server
from src.client import send_message

def run_server():
    logging.info("Starting the server thread.")
    start_server()

def test_server_client_interaction():
    logging.info("Initializing server thread.")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server time to start
    logging.info("Server thread started.")

    message = "Hello, Server!"
    logging.info(f"Sending message to server: {message}")
    response = send_message(message)
    logging.info(f"Received response from server: {response}")
    assert response == message
