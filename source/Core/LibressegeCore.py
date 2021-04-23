from Core.UPDconnections.UPDconnections import UPDconnections
from Core.Cryptography.Cryptography import Cryptography

class LibressegeCore():
    def __init__(self, dataDir):
        self.upd = UPDconnections()
        self.crypto = Cryptography(dataDir)

    def RSAgenrateKey(self):
        try:
            self.crypto.generateKey()
            self.crypto.exportKeys()
        except:
            pass

    def RSAimportKey(self):
        try:
            self.crypto.importKeys()
        except:
            pass

    def start(self, myIP, myPORT):
        try:
            self.upd.start(myIP, int(myPORT))
            return 0
        except:
            pass

    def connect(self, myName, serverIP, serverPORT = 9090):
        try:
            if serverIP != "":
                self.serverIP = serverIP
                self.serverPORT = int(serverPORT)
                self.myName = myName
                self.upd.sendData(str(self.myName).encode()+"////server".encode(), self.serverIP, self.serverPORT)
        except:
            pass

    def disconnect(self):
        try:
            self.upd.sendData("disconnect////server".encode(), self.serverIP, self.serverPORT)
        except:
            pass

    def getMessage(self):
        try:
            data = self.upd.getData()[0]
            return self.crypto.decrypt(data)
        except:
            return "Error"

    def sendMessage(self, data, recipientName, recipientKey):
        try:
            data = self.crypto.encrypt(str(data), recipientKey)+"////".encode()+recipientName.encode()
            self.upd.sendData(data, self.serverIP, self.serverPORT)
        except:
            pass
