from kivy.storage.jsonstore import JsonStore

from os.path import join

class addressBookHandler():
    def __init__(self, dataDir):
        self.addressBookJSON = JsonStore(join(dataDir, "addressBook.json"))

    def newAddress(self, name, key):
        self.addressBookJSON.put(name, RSA = key)

    def deleteAddress(self, name):
        self.addressBookJSON.delete(name)

    def getKey(self, name):
        return self.addressBookJSON.get(name).get("RSA")

    def getNames(self):
        return self.addressBookJSON.keys()

class connectBookHandler():
    def __init__(self, dataDir):
        self.connectBookJSON = JsonStore(join(dataDir, "connectBook.json"))
        if not(self.connectBookJSON.exists("Server from developers")):
            self.connectBookJSON.put("Server from developers", IP = "93.84.85.241", PORT = 9090)
    
    def newServer(self, name, ip, port):
        self.connectBookJSON.put(name, IP = ip, PORT = port)

    def deleteServer(self, name):
        self.connectBookJSON.delete(name)

    def getServer(self, name):
        return (self.connectBookJSON.get(name).get("IP"), self.connectBookJSON.get(name).get("PORT"))

    def getServers(self):
        return self.connectBookJSON.keys()

class dialogsBookHandler():
    def __init__(self, dataDir):
        self.dialogsBookJSON = JsonStore(join(dataDir, "dialogs.json"))

    def newDialog(self, name):
        self.dialogsBookJSON.put(name, dialog = "")

    def newMessage(self, name, message, sender):
        if str(self.dialogsBookJSON.get(name)["dialog"])=="":
            self.dialogsBookJSON.put(name, dialog=str(self.dialogsBookJSON.get(name)["dialog"])+str(sender)+": "+str(message))
        else:
            self.dialogsBookJSON.put(name, dialog=str(self.dialogsBookJSON.get(name)["dialog"])+"\/\/"+str(sender)+": "+str(message))

    def deleteDialog(self, name):
        self.dialogsBookJSON.delete(name)

    def getDialog(self, name):
        return self.dialogsBookJSON.get(name).get("dialog").split("\/\/")

    def getDialogs(self):
        return self.dialogsBookJSON.keys()