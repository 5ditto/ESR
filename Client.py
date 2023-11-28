import socket, sys, threading

from Packet import Packet
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender

# Como inciar o Cliente: Client.py 3 [ipBootstrapper] [portaBootstrapper] 

class Client:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = sys.argv[1]
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.gotVizinhos = threading.Event()
        self.vizinhos = []
        self.ipRP = ""

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"","",self)
        serverTCP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos


        for vizinho in self.vizinhos:
            packetFload = Packet(self.name,vizinho[1],4,[])
            TCPSender(packetFload,12345)



    def getIpRP(self):
        return self.ipRP
    
    def setIpRP(self,ip):
        self.ipRP = ip

    
    def setVizinhos(self,vizinhos):
        self.vizinhos = vizinhos
    
    def getVizinhos(self):
        return self.vizinhos

    def getNome(self):
        return self.name
    
    def getEventVizinhos(self):
        return self.gotVizinhos

    def getType(self):
        return self.type


client = Client()