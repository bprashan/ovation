import pytest
import threading
import time
from src.server import start_server
from src.client import send_message

def run_server():
    print("Starting the server thread.")
    start_server()

def test_server_client_interaction():
    print("Initializing server thread.")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server time to start
    print("Server thread started.")

    message = "Hello, Server!"
    print(f"Sending message to server: {message}")
    response = send_message(message)
    print(f"Received response from server: {response}")
    assert response == message