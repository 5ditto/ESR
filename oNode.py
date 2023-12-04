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
        serverUDP = UDPReceiver(self)
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

    # Adiciona ao dicionário para quem está a transmitir o nome do vídeo e o nodo
    def addATransmitir(self,nomeVideo,tuploVizinho):
        if nomeVideo in self.aTransmitir:
            self.aTransmitir[nomeVideo].append(tuploVizinho)
            if tuploVizinho not in self.aTransmitir[nomeVideo]:
                print("[STREAM UDP] Estou a transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
                print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)
        else:
            self.aTransmitir[nomeVideo] = [tuploVizinho]
            print("[STREAM UDP] Estou a transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
            print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)
    
    def getATransmitir(self):
        return self.aTransmitir

    def rmATransmitir(self,nomeVideo,tuploVizinho):
        self.aTransmitir[nomeVideo].remove(tuploVizinho)
        if tuploVizinho not in self.aTransmitir[nomeVideo]:
            print("[STREAM UDP] Parei de transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
            print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)


router = oNode()
