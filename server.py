import socket
import threading
import json
import os

HOST = "localhost"
PORT = 5000

clients = []


def broadcast(message, sender_conn=None):
    """
    Send a message to all connected clients except sender.
    """
    for client in clients:
        conn = client["conn"]

        if conn != sender_conn:
            try:
                conn.send(message.encode())
            except:
                pass


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        try:
            data = conn.recv(4096)

            if not data:
                break

            message = json.loads(data.decode())

            msg_type = message.get("type")

            if msg_type == "chat":

                username = message.get("username")
                text = message.get("message")

                print(f"[CHAT] {username}: {text}")

                response = {
                    "type": "chat",
                    "server_message": f"{username} says: {text}"
                }

                broadcast(json.dumps(response), conn)

            elif msg_type == "request":

                request = message.get("request")

                print(f"[REQUEST] {request}")

                response = {
                    "type": "response",
                    "message": f"Server received request: {request}"
                }

                conn.send(json.dumps(response).encode())

            elif msg_type == "file":

                filename = message.get("filename")
                content = message.get("content")

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"[FILE RECEIVED] {filename}")

                response = {
                    "type": "response",
                    "message": f"File '{filename}' received successfully."
                }

                conn.send(json.dumps(response).encode())

            elif msg_type == "disconnect":

                print(f"[DISCONNECT] {addr}")

                response = {
                    "type": "response",
                    "message": "Disconnected successfully."
                }

                conn.send(json.dumps(response).encode())
                break

            else:

                response = {
                    "type": "error",
                    "message": "Unknown command type."
                }

                conn.send(json.dumps(response).encode())

        except json.JSONDecodeError:

            error = {
                "type": "error",
                "message": "Invalid JSON format."
            }

            conn.send(json.dumps(error).encode())

        except Exception as e:

            print(f"[ERROR] {e}")
            break

    conn.close()

    for client in clients[:]:
        if client["conn"] == conn:
            clients.remove(client)

    print(f"[DISCONNECTED] {addr}")


def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen()

    print("=" * 50)
    print("TCP CHAT SERVER RUNNING")
    print(f"Listening on {HOST}:{PORT}")
    print("=" * 50)

    while True:

        conn, addr = server.accept()

        clients.append({
            "conn": conn,
            "addr": addr
        })

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()

        print(
            f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}"
        )


if __name__ == "__main__":
    start_server()