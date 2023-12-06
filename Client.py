import socket, sys, threading


from Packet import Packet
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender
from tkinter import Tk
from ClientGUI import ClientGUI


# Como inciar o Cliente: Client.py 3 [ipBootstrapper] [portaBootstrapper] 

class Client:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.vizinhos = []
        self.ipRP = ""
        self.videosDisponiveis = []

        self.gotVizinhos = threading.Event()
        self.gotIpRP = threading.Event()
        self.gotVideosDisponiveis = threading.Event()


        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"","",self)
        serverTCP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        self.gotIpRP.wait()     # espera receber o Ip do RP

        # Fazer fload na rede
        for vizinho in self.vizinhos:
            packetFload = Packet(self.name,vizinho[1],4,[])
            TCPSender(packetFload,12345)

        while 1:

            videoName = self.menuVideos()

            root = Tk()
            video = ClientGUI(root,self.name,self.ipRP,videoName)
            video.master.title("Cliente " + self.name)
            root.mainloop()




        



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
    

    def startfload(self):
        # Fazer fload na rede
        for vizinho in self.vizinhos:
            packetFload = Packet(self.name,vizinho[1],4,[])
            TCPSender(packetFload,12345)


    def menuVideos(self):
        print("+-------------------------+")
        print("|           MENU          |")
        print("+-------------------------+")
        print("| 1 - Vídeos Disponíveis  |")
        print("+-------------------------+")

        opcao = 0
        while opcao != 1:
            opcao = int(input("Selecione a opção: "))

        if opcao == 1:
            # Pede vídeo ao RP
            packetPedirVideo = Packet(self.name,self.ipRP,7,"Quais vídeos estão Disponíveis?")
            TCPSender(packetPedirVideo,12345)
            self.gotVideosDisponiveis.wait()
            self.printVideosDisponíveis()
            self.gotVideosDisponiveis.clear()
            video = ""
            while video not in self.videosDisponiveis:
                video = input("Selecione o vídeo: ")
            return video

            
                



        
    def printVideosDisponíveis(self):
        mensagem = "Videos Disponíveis: " + ", ".join(self.videosDisponiveis)
        print(mensagem)



client = Client()