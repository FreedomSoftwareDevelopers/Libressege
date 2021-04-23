from kivy.storage.jsonstore import JsonStore

from os.path import join

class addressBookHandler():
    def __init__(self, dataDir):
        self.addressBookJSON = JsonStore(join(dataDir, "addressBook.json"))

    def newAddress(self, name, key):
        self.addressBookJSON.put(name, RSA = key)

    def getKey(self, name):
        return self.addressBookJSON.get(name).get("RSA")
