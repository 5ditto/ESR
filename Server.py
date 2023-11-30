import socket, sys,threading


from TCPSender import TCPSender
from UDPReceiver import UDPReceiver
from VideoStream import VideoStream
from TCPReceiver import TCPReceiver
from Packet import Packet

# Como inciar o Servidor: Server.py 4 [ipBootstrapper] [portaBootstrapper] [nomeVideo] [nomeVideo] ...


class Server:
    
    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.videosName = sys.argv[4:]
        self.gotVizinhos = threading.Event()
        self.gotIpRP = threading.Event()
        self.vizinhos = []
        self.ipRP = ""
        self.aTransmitir = {}

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"",self,"")
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver()
        serverUDP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos


        self.gotIpRP.wait()     # espera receber o Ip do RP


        # Diz ao RP quais os vídeos que tem
        packetServer = Packet(self.name, self.ipRP,6,self.videosName)
        TCPSender(packetServer,12345)

        # Fazer fload na rede
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

    def getEventIpRP(self):
        return self.gotIpRP


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



server = Server()