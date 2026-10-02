import json
import os
import socket
import threading
from pathlib import Path

from cipher import decrypt, encrypt
from dotenv import load_dotenv

env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)

NODE_NAME = os.getenv("NODE_NAME", Path(__file__).parent.name)
SECRET_KEY = os.environ["SECRET_KEY"]
LISTEN_HOST = os.environ["LISTEN_HOST"]
LISTEN_PORT = int(os.environ["LISTEN_PORT"])
TARGET_HOST = os.environ["TARGET_HOST"]
TARGET_PORT = int(os.environ["TARGET_PORT"])

def receive_all(connection):
    data = bytearray()
    while True:
        chunk = connection.recv(4096)
        if not chunk:
            return bytes(data)
        data.extend(chunk)

def handle_message(connection, address):
    try:
        data = receive_all(connection)
        packet = json.loads(data.decode("utf-8"))
        plaintext = decrypt(packet["ciphertext"], SECRET_KEY)

        print("\n")
        print(f"Message from : {packet['sender']} ({address[0]})")
        print(f"Ciphertext : {packet['ciphertext']}")
        print(f"Plaintext  : {plaintext}")
        print("\n")

        print("Message: ", end="", flush=True)
    except Exception as error:
        print(f"\nPackage from {address[0]} rejected: {error}")
    finally:
        connection.close()

def listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LISTEN_HOST, LISTEN_PORT))
        server.listen()
        print(f"{NODE_NAME} listening on {LISTEN_HOST}:{LISTEN_PORT}...")

        while True:
            connection, address = server.accept()
            threading.Thread(
                target=handle_message,
                args=(connection, address),
                daemon=True,
            ).start()


def send_message(plaintext):
    ciphertext = encrypt(plaintext, SECRET_KEY)
    packet = {
        "sender": NODE_NAME,
        "ciphertext": ciphertext,
    }
    data = json.dumps(packet).encode("utf-8")

    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5) as connection:
        connection.sendall(data)

    print(f"Ciphertext sent: {ciphertext}")


def main():
    if len(SECRET_KEY.encode("utf-8")) != 8:
        raise ValueError("SECRET_KEY must be 8 bytes long.")

    threading.Thread(target=listen, daemon=True).start()

    print(f"To: {TARGET_HOST}:{TARGET_PORT}")

    while True:
        try:
            message = input("Message: ")

            if not message:
                continue
            send_message(message)
        except (ConnectionError, OSError, ValueError) as error:
            print(f"Failed to send message: {error}")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
