import socket
import sys
import threading
import time

from Packet import Packet
from Bootstrapper import Bootstrapper 
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender
from TCPBootstrapper import TCPBootstrapper

# Caso o nodo seja Bootstrapper: Router.py 1 [ficheiroBootstrapper] [porta]
# Caso o nodo seja Router: Router.py 0 [ipBoostrapper] [portaBootstrapper]
# Caso o nodo seja Cliente: Router.py 3 [ipBoostrapper] [portaBootstrapper]
# Caso o nodo seja RP: Router.py 0 [ipBoostrapper] [portaBootstrapper]

class Router:

    def __init__(self):
        self.vizinhos = []
        self.nome = socket.gethostname()
        self.type = (sys.argv[1])
        self.GotVizinhos = threading.Event()        # tem que aguardar até que possua os vizinhos

        if self.type == "1":    # Sou o Bootstrapper
            file = sys.argv[2]
            porta = int(sys.argv[3])
            bootstrapper = Bootstrapper(file)
            self.vizinhos = bootstrapper.getVizinhos(self.nome)  

            # thread apenas para o bootstrap
            threadBootstrapper = threading.Thread(target=TCPBootstrapper,args = (porta,bootstrapper))
            threadBootstrapper.start()


        # colocar servidor à escuta
        threadTCPRecieve = threading.Thread(target=TCPReceiver,args = (self,))
        threadTCPRecieve.start()
        
        if self.type != "1":    # Não é o Bootstrapper

            ipBootstrapper = sys.argv[2]
            portaBootstrapper = int(sys.argv[3])
            
            # Pedir Vizinhos ao Bootstrapper
            packet = Packet(self.nome,ipBootstrapper,1,self.nome)
            TCPSender(packet,portaBootstrapper)
            self.GotVizinhos.wait()     # espera receber os vizinhos

        

        
        if self.type == "2":    # Sou o RP
            print("SOU O RP")
        
        if self.type == "3":    # Sou um cliente
            
            # começar a fazer fload
            for vizinho in self.vizinhos:
                packet = Packet(self.nome,vizinho[1],4,[])
                TCPSender(packet,12345)


    

    def setVizinhos(self,vizinhos):
        self.vizinhos = vizinhos
    
    def getVizinhos(self):
        return self.vizinhos

    def getType(self):
        return self.type
    
    def getNome(self):
        return self.nome

    def getEventVizinhos(self):
        return self.GotVizinhos
    

router = Router()
