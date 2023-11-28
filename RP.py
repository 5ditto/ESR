import socket, sys, threading

from Packet import Packet
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender

# Como inciar o RP: RP.py 2 [ipBootstrapper] [portaBootstrapper]

class RP:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = sys.argv[1]
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.gotVizinhos = threading.Event()
        self.vizinhos = []
        self.arvore = {}        # dicionario com um array de caminhos (arrays)
        self.nodosATransmitir = {}


        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,self,"","")
        serverTCP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        # Envia para o Bootstrapper a dizer que é o RP
        packetIpRP = Packet(self.name,self.ipBootstrapper,5,self.name)
        TCPSender(packetIpRP,self.portaBootstrapper)


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


    # adiciona um caminho à árvore do tipo "('n7',[('n1','10.0.0.1'),('n7','10.0.3.20')])"
    def adicionaCaminho(self,caminho):
            if caminho[0] in self.arvore:
                self.arvore[caminho[0]].append(caminho[1])
            else:
                self.arvore[caminho[0]] = [caminho[1]]
            print(self.arvore)

    

rp = RP()