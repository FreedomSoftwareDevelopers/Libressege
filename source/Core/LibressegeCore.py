from Core.UPDconnections.UPDconnections import UPDconnections
from Core.Cryptography.Cryptography import Cryptography

class LibressegeCore():
    def __init__(self, dataDir):
        self.upd = UPDconnections()
        self.crypto = Cryptography(dataDir)

    def RSAgenrateKey(self):
        self.crypto.generateKey()
        self.crypto.exportKeys()

    def RSAimportKey(self):
        self.crypto.importKeys()

    def start(self, myIP, myPORT):
        self.upd.start(myIP, int(myPORT))
        return 0

    def connect(self, myName, serverIP, serverPORT = 9090):
        if serverIP != "":
            self.serverIP = serverIP
            self.serverPORT = int(serverPORT)
            self.myName = myName
            self.upd.sendData(str(self.myName).encode()+"////server".encode(), self.serverIP, self.serverPORT)

    def disconnect(self):
        self.upd.sendData("disconnect////server".encode(), self.serverIP, self.serverPORT)

    def getMessage(self):
        data = self.upd.getData()[0]
        return self.crypto.decrypt(data)

    def sendMessage(self, data, recipientName, recipientKey):
        data = self.crypto.encrypt(str(data), recipientKey)+"////".encode()+recipientName.encode()
        self.upd.sendData(data, self.serverIP, self.serverPORT)
