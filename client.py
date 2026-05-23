import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 5050))

client.send("Hello Server!".encode())

response = client.recv(1024).decode()

print("Server says", response)

client.close()