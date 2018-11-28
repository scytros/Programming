from Crypto.Cipher import AES
from Crypto import Random

key = "Sixteen byte key".encode()
iv = Random.new().read(AES.block_size)


def encrypt(data):
    """Encrypts the data that has been send, and returns an encrypted string"""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    text = cipher.encrypt(data)

    return text


def decrypt(data):
    """Decrypts the data that has been send, and returns decrypted string"""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    plainText = cipher.decrypt(data)

    return plainText