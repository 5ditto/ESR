import socket, sys, threading


from Packet import Packet
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender
from UDPReceiver import UDPReceiver

# Como inciar o Cliente: Client.py 3 [ipBootstrapper] [portaBootstrapper] 

class Client:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.gotVizinhos = threading.Event()
        self.gotIpRP = threading.Event()
        self.gotVideosDisponiveis = threading.Event()
        self.vizinhos = []
        self.ipRP = ""
        self.videosDisponiveis = []
        self.nodosAtivos = {} 

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"","",self)
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver()
        serverUDP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        self.gotIpRP.wait()     # espera receber o Ip do RP

        # Fazer fload na rede
        for vizinho in self.vizinhos:
            packetFload = Packet(self.name,vizinho[1],4,[])
            TCPSender(packetFload,12345)

        self.menuVideos()




        



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

    def getEventVideosDisponiveis(self):
        return self.gotVideosDisponiveis
    

    def setVideosDisponiveis(self,videos):
        self.videosDisponiveis = videos
    

    def menuVideos(self):
        print("+-------------------------+")
        print("|           MENU          |")
        print("+-------------------------+")
        print("| 1 - Vídeos Disponíveis  |")
        print("+-------------------------+")
        if int(input()) == 1:
            # Pede vídeo ao RP
            packetPedirVideo = Packet(self.name,self.ipRP,7,"Quais vídeos estão Disponíveis?")
            TCPSender(packetPedirVideo,12345)
            self.gotVideosDisponiveis.wait()
            self.printVideosDisponíveis()
            video = ""
            while video not in self.videosDisponiveis:
                video = input("Selecione o vídeo: ")
            packetVideo = Packet(self.name, self.ipRP,9,video)
            TCPSender(packetVideo,12345)
            
                



        
    def printVideosDisponíveis(self):
        mensagem = "Videos Disponíveis: " + ", ".join(self.videosDisponiveis)
        print(mensagem)



client = Client()