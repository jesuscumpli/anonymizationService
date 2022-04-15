import secrets
from cryptography.fernet import Fernet
import os


def generate_encryption_key():
    dir = os.path.dirname(os.path.abspath(__file__))
    key = Fernet.generate_key()
    with open(dir + "/encription_key.bin", "wb") as binary_file:
        binary_file.write(key)


def load_encription_key():
    dir = os.path.dirname(os.path.abspath(__file__))
    file = open(dir + "/encription_key.bin", "rb")
    key = file.read()
    return key


def generate_secret_key():
    dir = os.path.dirname(os.path.abspath(__file__))
    key = secrets.token_bytes(32)
    with open(dir + "/secret_key.bin", "wb") as binary_file:
        binary_file.write(key)


def load_secret_key():
    dir = os.path.dirname(os.path.abspath(__file__))
    file = open(dir + "/secret_key.bin", "rb")
    key = file.read()
    return key
