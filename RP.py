import socket, sys, threading

from Packet import Packet
from TCPReceiver import TCPReceiver
from TCPSender import TCPSender
from UDPReceiver import UDPReceiver

# Como inciar o RP: RP.py 2 [ipBootstrapper] [portaBootstrapper]

class RP:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.gotVizinhos = threading.Event()
        self.vizinhos = []
        self.arvore = {}        # dicionario com um array de caminhos (arrays)
        self.servidores = {}    # para saber quais os servidores com os videos que tem ex: {'n1':['videoA','videoB']}
        self.nodosAtivos = {}       # dicionario com os nodos ativos e os videos que estão a reproduzir
        self.ipRP = ""
        self.gotIpRP = threading.Event()
        self.aTransmitir = {}

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,self,"","")
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver()
        serverUDP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        self.gotIpRP.wait()


        # Quando receber pedido para o Servidor enviar o video mostrar a árvore que possui e selecionar 
        # o caminho mais próximo através de saltos para já

        # depois mandar mensagem a todos os nodos para onde é que devem enviar o pacote de video
        # enviar o pacote de vídeo até ao cliente 


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

    def addServidor(self,server,videos):
        self.servidores[server] = videos
    
    def setIpRP(self,ip):
        self.ipRP = ip

    def getEventIpRP(self):
        return self.gotIpRP


    # adiciona um caminho à árvore do tipo "('n7',[('n1','10.0.0.1'),('n7','10.0.3.20')])"
    def adicionaCaminho(self,caminho):
            if caminho[0] in self.arvore:
                if caminho[1] not in self.arvore[caminho[0]]:
                    self.arvore[caminho[0]].append(caminho[1])
            else:
                self.arvore[caminho[0]] = [caminho[1]]

    

    def printArvore(self):
        print("+----------------+")
        print("|     ÁRVORE     |")
        print("+----------------+")

        nodoanterior = ""
        for nodo, caminhos in self.arvore.items():
            for caminho in caminhos:
                if nodo != nodoanterior:
                    print()
                print("--------")
                print(f"|  {nodo}  |  {caminho}")
                print("--------")
                nodoanterior = nodo


    def getVideosDisponiveis(self):
        videosDisponiveis = []
        for server, videos in self.servidores.items():
            for video in videos:
                if video not in videosDisponiveis:
                    videosDisponiveis.append(video)
        return videosDisponiveis





    def melhorCaminho(self,cliente,nomeVideo):
        melhorCaminho  = []
        size = 9999
        #caminhosTotal = []
        servidoresComVideo = []
        # Quais servidores têm o vídeo:
        for server, videos in self.servidores.items():
            if nomeVideo in videos:
                servidoresComVideo.append(server)

        caminhosCliente = self.arvore[cliente]
        caminhosServidor = self.caminhosServidor(servidoresComVideo)
        for caminhoCliente in caminhosCliente:
            for caminhoServidor in caminhosServidor:
                #self.caminhoClienteServidor(caminhoCliente,caminhoServidor,caminhosTotal)
                 melhorCaminho,size = self.caminhoClienteServidor(caminhoCliente, caminhoServidor,melhorCaminho,size,nomeVideo) # para já por saltos
        self.adddNodosAtivo(melhorCaminho,nomeVideo)
        print(melhorCaminho[::-1])
        print(self.nodosAtivos)
        return melhorCaminho[::-1]
    


    def caminhoClienteServidor(self, caminhoCliente, caminhoServidor,melhorCaminho,size,nomeVideo):
        caminhoClienteAux = caminhoCliente + [(self.name,self.ipRP)] + caminhoServidor[::-1]
        if len(caminhoClienteAux) < size:
            melhorCaminho = caminhoClienteAux
            size = len(melhorCaminho)

        # Quando há nodos já a transmitir o vídeo        
        for nodoC in caminhoClienteAux:
            if nodoC in self.nodosAtivos:
                if nomeVideo in self.nodosAtivos[nodoC]:
                    indexNA = caminhoClienteAux.index(nodoC)
                    newCaminho = caminhoClienteAux[:indexNA + 1]
                    if len(newCaminho) < size:
                        melhorCaminho = newCaminho
                        size = len(melhorCaminho)
        
        # Quando há um melhor caminho que não passe pelo RP
        for nodoC in caminhoCliente:
                if nodoC in caminhoServidor:
                    indexS = caminhoServidor.index(nodoC)
                    indexC = caminhoCliente.index(nodoC)
                    caminhoC = caminhoCliente[:indexC + 1]
                    caminhoS = caminhoServidor[indexS:][::-1]
                    caminhoClienteAux = caminhoC + caminhoS
                    if len(caminhoClienteAux < size):
                        melhorCaminho = caminhoClienteAux
                        size = len(melhorCaminho)
        return (melhorCaminho,size)


    # Calcula todos os caminhos possíveis
    #def caminhoClienteServidor(self, caminhoCliente, caminhoServidor,caminhosTotal):
    #    caminhoClienteAux = caminhoCliente + [('RP','0.0.0.0')]
    #    caminhosTotal.append(caminhoClienteAux + caminhoServidor[::-1])
    #    for nodoC in caminhoCliente:
    #            if nodoC in caminhoServidor:
    #                indexS = caminhoServidor.index(nodoC)
    #                indexC = caminhoCliente.index(nodoC)
    #                caminhoC = caminhoCliente[:indexC + 1]
    #                caminhoS = caminhoServidor[indexS:][::-1]
    #                caminhosTotal.append(caminhoC+ caminhoS)

    def caminhosServidor(self,servidores):
        caminhosTotal = []
        for nomeServidor, caminhos in self.arvore.items():
            if nomeServidor in servidores:
                caminhosTotal += caminhos
        return caminhosTotal
        
    def adddNodosAtivo(self,caminho,video):
        for nodo in caminho:
            if nodo in self.nodosAtivos:
                if video not in self.nodosAtivos[nodo]:
                    self.nodosAtivos[nodo].append(video)
            else:
                self.nodosAtivos[nodo] = [video]        
    
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








rp = RP()