from Core.UPDconnections.UPDconnections import UPDconnections

class LibressegeServerCore():
    def __init__(self):
        self.upd = UPDconnections()
        self.addresses = []

    def start(self, myIP, myPORT):
        self.upd.start(myIP, myPORT)
        return 0

    def handler(self):
        data, addr = self.upd.getData()
        data, recipient = data.split("////".encode())
        if recipient == "server".encode():
            if data == "disconnect".encode():
                addressID = 0
                for address in self.addresses:
                    if (address["IP"], address["PORT"]) == (addr[0], addr[1]):
                        self.addresses.pop(addressID)
                        break
                    addressID += 1
                return 0
            else:
                self.addresses.append({"Name": data.decode(), "IP": addr[0], "PORT": addr[1]})
                return 0
        else:
            for address in self.addresses:
                if address["Name"].encode() == recipient:
                    self.sendMessage(data, address["IP"], int(address["PORT"]))
                    break
            return 0

    def sendMessage(self, data, recipientIP, recipientPORT):
        self.upd.sendData(data, recipientIP, recipientPORT)