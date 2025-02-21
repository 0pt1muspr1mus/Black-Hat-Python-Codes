import socket
import threading

ip = "0.0.0.0"
port = 12345

stop_server = False

def handle_client(client_sock):
    global stop_server
    with client_sock as sock:
        try:
            while True:
                req = sock.recv(1024)
                if not req:
                    print("Connection closed by client")
                    stop_server = True
                    break  
                
                msg = req.decode().strip()
                if msg.lower() == "exit":  
                    print("Client requested to stop server.")
                    sock.send(b'Good Bye...')
                    stop_server = True
                    break
                else:
                    print("Received from Client:", msg)
                    sock.send(b'ACK')

        except ConnectionResetError:
            print("Connection closed by Client")
            stop_server = True

        finally:
            sock.close()

def main():
    global stop_server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)

    print("Listening on", ip, "port", port)

    while not stop_server:  # Keep running until stop_server is True
        try:
            server.settimeout(1)  # Allows checking stop_server every second
            client, addr = server.accept()
            print("Accepted connection from:", addr[0], addr[1])
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
        except socket.timeout:
            continue  # Check the stop flag again

    print("Shutting down server...")
    server.close()

if __name__ == '__main__':
    main()
