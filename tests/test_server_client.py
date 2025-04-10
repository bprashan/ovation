import threading
import time
from src.server import start_server
from src.client import send_message

def run_server():
    start_server()

def test_server_client_interaction():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Allow server time to start

    message = "Hello, Server!"
    response = send_message(message)
    assert response == message

