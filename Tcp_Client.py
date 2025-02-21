import socket

target_host = "127.0.0.1"
tareget_port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, tareget_port))

while True:
    msg = input("Enter Message to send to Server: ")
    client.send(msg.encode())
    response = client.recv(4096)
    print(response.decode())
    ch = input("Do you want to continue chatting...(y/n)")
    if ch != 'y':
        break

client.close()