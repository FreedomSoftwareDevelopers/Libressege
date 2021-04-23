import socket

class UPDconnections():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self, socketIP,socketPORT):
        self.socket.bind((socketIP, socketPORT))

    def sendData(self, data, recipientIP, recipientPORT):
        self.socket.sendto(data, (recipientIP, recipientPORT))

    def getData(self, packetSizeKB = 1):
        data, addr = self.socket.recvfrom(packetSizeKB*1024)
        return (data, addr) 
