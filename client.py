import socket
import json
import os

HOST = "localhost"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))

    print("=" * 50)
    print("CONNECTED TO SERVER")
    print("=" * 50)

except Exception as e:
    print("Connection failed:", e)
    exit()

username = input("Enter username: ")


while True:

    print("\nChoose Option")
    print("1. Chat Message")
    print("2. Send File")
    print("3. Send Request")
    print("4. Disconnect")

    choice = input("Choice: ")

    try:

        if choice == "1":

            text = input("Message: ")

            message = {
                "type": "chat",
                "username": username,
                "message": text
            }

            client.send(
                json.dumps(message).encode()
            )

        elif choice == "2":

            filepath = input(
                "Enter text file path: "
            )

            if not os.path.exists(filepath):
                print("File not found.")
                continue

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

            message = {
                "type": "file",
                "filename": os.path.basename(filepath),
                "content": content
            }

            client.send(
                json.dumps(message).encode()
            )

            response = client.recv(4096)

            print(
                json.loads(
                    response.decode()
                )["message"]
            )

        elif choice == "3":

            request_text = input(
                "Enter request: "
            )

            message = {
                "type": "request",
                "request": request_text
            }

            client.send(
                json.dumps(message).encode()
            )

            response = client.recv(4096)

            print(
                json.loads(
                    response.decode()
                )["message"]
            )

        elif choice == "4":

            message = {
                "type": "disconnect"
            }

            client.send(
                json.dumps(message).encode()
            )

            response = client.recv(4096)

            print(
                json.loads(
                    response.decode()
                )["message"]
            )

            break

        else:

            print("Invalid option.")

    except Exception as e:

        print("Error:", e)

client.close()

print("Client closed.")