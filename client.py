import socket
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 5050))

data = {
    "username": "Thando",
    "message": "Hello Server!"
}

client.send(json.dumps(data).encode())

#client.send("Hello Server!".encode())

response = client.recv(1024).decode()

#print("Server says", response)
print(response)

client.close()