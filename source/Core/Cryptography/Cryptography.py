from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from kivy.storage.jsonstore import JsonStore

from os.path import join

class Cryptography():
    def __init__(self, dataDir):
        self.RSAJSON = JsonStore(join(dataDir, "RSAKeys.json"))

    def generateKey(self, code = "code"):
        key = RSA.generate(2048)
        self.privateKeyRSA = key.exportKey(
            passphrase = code,
            pkcs = 8,
            protection="scryptAndAES128-CBC"
        )
        self.publicKeyRSA = key.publickey().exportKey()

    def exportKeys(self):
        self.RSAJSON.put("private", RSA = self.privateKeyRSA.decode())
        self.RSAJSON.put("public", RSA = self.publicKeyRSA.decode())

    def importKeys(self):
        self.privateKeyRSA = self.RSAJSON.get("private").get("RSA").encode()
        self.publicKeyRSA = self.RSAJSON.get("public").get("RSA").encode()

    def encrypt(self, data, publicKeyRSA):
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(publicKeyRSA.encode()))
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode("utf8"))
        ff = cipher_rsa.encrypt(session_key)
        data = ff + "****".encode() + cipher_aes.nonce + "****".encode() + tag + "****".encode() + ciphertext
        return data

    def decrypt(self, data, code = "code"):
        enc_session_key, nonce, tag, ciphertext = data.split("****".encode())
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(self.privateKeyRSA, passphrase = code))
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode("utf8")

    def getKey(self):
        return self.publicKeyRSA
