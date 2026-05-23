import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("localhost", 5050))

server.listen(1)

print("Sever listening on port 5050....")

conn, addr = server.accept()

print(f"Connected by {addr}")

message = conn.recv(1024).decode()

print("Client says:, message")

conn.send("Hello from server!".encode())

conn.close
