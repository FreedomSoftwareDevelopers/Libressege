from Core.GhostConnect.GhostConnect import GhostConnect

class LibressegeCore():
    def __init__(self, dataDir):
        self.GhostConnect = GhostConnect(dataDir)

    def RSAgenrateKey(self):
        try:
            self.GhostConnect.generateKey()
            self.GhostConnect.exportKeys()
        except:
            pass

    def RSAimportKey(self):
        try:
            self.GhostConnect.importKeys()
        except:
            pass

    def start(self, myIP, myPORT):
        try:
            self.GhostConnect.startUPD(myIP, int(myPORT))
        except:
            pass

    def connect(self, myName, serverIP, serverPORT = 9090):
        try:
            if serverIP != "":
                self.serverIP = serverIP
                self.serverPORT = int(serverPORT)
                self.myName = myName
                self.GhostConnect.sendData(str(self.myName).encode()+"////server".encode(), self.serverIP, self.serverPORT)
        except:
            pass

    def disconnect(self):
        try:
            self.GhostConnect.sendData("disconnect////server".encode(), self.serverIP, self.serverPORT)
        except:
            pass

    def getMessage(self):
        try:
            return self.GhostConnect.decrypt(self.GhostConnect.getData()[0])
        except:
            return "Error"

    def sendMessage(self, data, recipientName, recipientKey):
        try:
            self.GhostConnect.sendData(self.GhostConnect.encrypt(str(data), recipientKey)+"////".encode()+recipientName.encode(), self.serverIP, self.serverPORT)
        except:
            pass
