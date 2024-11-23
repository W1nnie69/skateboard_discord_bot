import socket
import threading
import time
import rsa
import sys
from select import select

HEADER = 1024
PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
PASSPHRASE = "IAMGAY"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Load private key once at the start
with open("networking\private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)


            msg = conn.recv(msg_length)

            try: #checks for !DISCONNECT msg to close socket
                decoded_msg = msg.decode(FORMAT)
                if decoded_msg == DISCONNECT_MSG:
                    connected = False

                socket_close_msg = "Socket has been closed"
                conn.send(socket_close_msg.encode(FORMAT))
                print(f"Socket [{addr}] has been closed.")

            except UnicodeDecodeError: #Encrypted data goes here
                print(f"[{addr}] Received binary data: {msg}")

                clear_message = rsa.decrypt(msg, private_key)
                clear_message = clear_message.decode(FORMAT)

                print("")
                print(clear_message)

                if clear_message == PASSPHRASE:
                    reply = "Server is alive"
                    conn.send(reply.encode(FORMAT))

                else:
                    conn.close()


    conn.close()


def start():
    
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while 2:
        server.listen()
        ready, _, _ = select([server], [], [], 2)

        if ready:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1} Connections")

        else:
            pass

print("[STARTING] Server is starting...")
start()