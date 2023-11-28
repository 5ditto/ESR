import socket, sys,threading

from TCPSender import TCPSender
from VideoStream import VideoStream
from TCPReceiver import TCPReceiver
from Packet import Packet

# Como inciar o Servidor: Server.py 4 [ipBootstrapper] [portaBootstrapper] [nomeVideo]


class Server:
    
    def __init__(self):
        self.name = socket.gethostname()
        self.type = sys.argv[1]
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.videoName = sys.argv[4]
        self.gotVizinhos = threading.Event()
        self.videoStream = VideoStream(self.videoName)
        self.ON = False
        self.vizinhos = []
        self.ipRP = ""

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"",self,"")
        serverTCP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos



    

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



server = Server()