import socket


def start_server(host='127.0.0.1', port=65432):
    print(f"Starting server on {host}:{port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Server is listening for incoming connections")
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    print("No data received. Closing connection.")
                    break
                print(f"Received data: {data.decode()}")
                conn.sendall(data)
                print("Sent data back to client")