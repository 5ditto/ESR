import socket, sys, threading

from Packet import Packet 
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender
from UDPReceiver import UDPReceiver



# Como iniciar o oNode: oNode.py 0 [ipBoostrapper] [portaBootstrapper] 


class oNode:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.gotVizinhos = threading.Event()
        self.vizinhos = []
        self.aTransmitir = {}



        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"","","")
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver()
        serverUDP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        





    def setVizinhos(self,vizinhos):
        self.vizinhos = vizinhos
    
    def getVizinhos(self):
        return self.vizinhos

    def getType(self):
        return self.type
    
    def getNome(self):
        return self.name

    def getEventVizinhos(self):
        return self.gotVizinhos
    
    def addATransmitir(self,nomeVideo,tuploVizinho):
        if nomeVideo in self.aTransmitir:
            self.aTransmitir[nomeVideo].append(tuploVizinho)
        else:
            self.aTransmitir[nomeVideo] = [tuploVizinho]

    def rmATransmitir(self, nomeVideo, tuploVizinho):
        if nomeVideo in self.aTransmitir:
            if tuploVizinho in self.aTransmitir[nomeVideo]:
                self.aTransmitir[nomeVideo].remove(tuploVizinho)
                if not self.aTransmitir[nomeVideo]:
                    del self.aTransmitir[nomeVideo]



router = oNode()
