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
    """Membaca satu paket sampai sender menutup koneksi."""
    data = bytearray()
    while True:
        chunk = connection.recv(4096)
        if not chunk:
            return bytes(data)
        data.extend(chunk)


def handle_message(connection, address):
    """Membaca paket, lalu mendekripsi ciphertext yang diterima."""
    try:
        data = receive_all(connection)
        packet = json.loads(data.decode("utf-8"))
        plaintext = decrypt(packet["ciphertext"], SECRET_KEY)

        print("\n")
        print(f"Pesan dari : {packet['sender']} ({address[0]})")
        print(f"Ciphertext : {packet['ciphertext']}")
        print(f"Plaintext  : {plaintext}")
        print("\n")

        print("Pesan: ", end="", flush=True)
    except Exception as error:
        print(f"\nPaket dari {address[0]} ditolak: {error}")
    finally:
        connection.close()


def listen():
    """Menunggu pesan masuk pada port milik node ini."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((LISTEN_HOST, LISTEN_PORT))
        server.listen()
        print(f"{NODE_NAME} mendengarkan di {LISTEN_HOST}:{LISTEN_PORT}")

        while True:
            connection, address = server.accept()
            threading.Thread(
                target=handle_message,
                args=(connection, address),
                daemon=True,
            ).start()


def send_message(plaintext):
    """Mengenkripsi lalu mengirim satu paket ke node tujuan."""
    ciphertext = encrypt(plaintext, SECRET_KEY)
    packet = {
        "sender": NODE_NAME,
        "ciphertext": ciphertext,
    }
    data = json.dumps(packet).encode("utf-8")

    with socket.create_connection((TARGET_HOST, TARGET_PORT), timeout=5) as connection:
        connection.sendall(data)

    print(f"Ciphertext terkirim: {ciphertext}")


def main():
    if len(SECRET_KEY.encode("utf-8")) != 8:
        raise ValueError("SECRET_KEY harus tepat 8 byte.")

    threading.Thread(target=listen, daemon=True).start()

    print(f"Tujuan: {TARGET_HOST}:{TARGET_PORT}")
    print("Key hanya dibaca secara lokal dan tidak dikirim.")
    print("Ketik /quit untuk keluar.\n")

    while True:
        try:
            message = input("Pesan: ")
            if message.strip().lower() == "/quit":
                break
            if not message:
                continue
            send_message(message)
        except (ConnectionError, OSError, ValueError) as error:
            print(f"Gagal mengirim: {error}")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
