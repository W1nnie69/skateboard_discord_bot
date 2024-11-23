import socket
import rsa
import time

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER = "10.1.0.150"
ADDR = (SERVER, PORT)


# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

def encrypt_secret(msg):
    with open("public.pem", "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())

    encrypted_msg = rsa.encrypt(msg.encode(), public_key)
    
    print(encrypted_msg)
    send(encrypted_msg)


def send(encrypted_msg):
    # message = encrypted_msg.encode(FORMAT)
    if isinstance(encrypted_msg, str):
        encrypted_msg = encrypted_msg.encode(FORMAT)

    msg_length = len(encrypted_msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER -len(send_length))
    client.send(send_length)
    client.send(encrypted_msg)

    response = client.recv(HEADER).decode(FORMAT)  
    print(f"Server responded: {response}")

   
while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    encrypt_secret("IAMGAY")
    send(DISCONNECT_MSG)
    time.sleep(5)
