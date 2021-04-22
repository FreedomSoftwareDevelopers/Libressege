from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

class Cryptography():
    def __init__(self):
        pass

    def generateKey(self, code):
        key = RSA.generate(2048)
        self.privateKeyRSA = key.exportKey(
            passphrase = code,
            pkcs = 8,
            protection="scryptAndAES128-CBC"
        )
        self.publicKeyRSA = key.publickey().exportKey()

    def exportKeys(self):
        with open('privateKeyRSA.pem', 'wb') as f:
            f.write(self.privateKeyRSA)
        with open('publicKeyRSA.pem', 'wb') as f:
            f.write(self.publicKeyRSA)

    def importKeys(self):
        self.privateKeyRSA = open('privateKeyRSA.pem').read()
        self.publicKeyRSA = open('publicKeyRSA.pem').read()

    def encrypt(self, data, publicKeyRSA):
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(publicKeyRSA))
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode("utf8"))
        data = cipher_rsa.encrypt(session_key) + "****".encode('utf-8') + cipher_aes.nonce + "****".encode('utf-8') + tag + "****".encode('utf-8') + ciphertext
        return data

    def decrypt(self, data, code):
        enc_session_key, nonce, tag, ciphertext = data.split("****".encode("utf8"))
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.privateKeyRSA, passphrase = code))
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode("utf8")

    def getKey(self):
        return self.publicKeyRSA 
