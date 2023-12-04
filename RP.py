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

        self.nodosAtivos = {}
        self.clientesAtivos = {}    # guarda o cliente e o vídeo e o caminho até ao cliente  
        self.arvore = {}        # dicionario com um array de caminhos (arrays)
        self.videos = {}
        self.ipRP = ""
        self.gotIpRP = threading.Event()
        self.aTransmitir = {}

        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,self,"","")
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver(self)
        serverUDP.start()

        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos

        self.gotIpRP.wait()




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


    def addVideos(self,server,videos):
        for video in videos:
            if video not in self.videos:
                self.videos[video] = server
    
    def setIpRP(self,ip):
        self.ipRP = ip

    def getEventIpRP(self):
        return self.gotIpRP

    def getVideos(self):
        return self.videos

    def getNodosAtivos(self):
        return self.nodosAtivos

    # adiciona um caminho à árvore do tipo "('n7',[('n1','10.0.0.1'),('n7','10.0.3.20')])"
    def adicionaCaminho(self,cliente, caminho):
            
            
            if cliente in self.arvore:

                for caminhoArvore in self.arvore[cliente]:
                    if self.compararCaminho(caminho,caminhoArvore):
                        self.arvore[cliente].remove(caminhoArvore)
                        self.arvore[cliente].append(caminho)
                        return
                self.arvore[cliente].append(caminho)
                    

            else:
                self.arvore[cliente] = [caminho]

    def compararCaminho(self,caminhoAtual,caminho):
        caminhoArvore = [triplo[0] for triplo in caminho]
        caminhoNovo = [triplo[0] for triplo in caminhoAtual]
        if caminhoArvore == caminhoNovo:
            return True
        else:
            return False
    

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
        return list(self.videos.keys())



    def melhorCaminho(self,nomeCliente, nomeVideo):
        melhorCaminho = []
        latencia = 999999.99
        caminhosCliente = self.arvore[nomeCliente]

        for caminho in caminhosCliente:

            # verificar se há nodo a transmitir
            if nomeVideo in list(self.nodosAtivos.keys()):  #  [movie.Mjpeg]
                nodosAtivos = self.nodosAtivos[nomeVideo]   # [(n3,111),(n1,111),(n2,111)]
                for triplo in caminho:            #[n11,n2,n1]
                    nodo = (triplo[0],triplo[1])
                    if nodo in nodosAtivos:

                        caminhoAtivo = caminho[:caminho.index(triplo) + 1]        # ERRO
                        if self.calculaLatencia(caminhoAtivo) < latencia:
                            latencia = self.calculaLatencia(caminhoAtivo)
                            melhorCaminho = [(triplo[0], triplo[1]) for triplo in caminhoAtivo]
            
            else:
                if self.calculaLatencia(caminho) < latencia:
                    latencia = self.calculaLatencia(caminho)
                    melhorCaminho = [(triplo[0], triplo[1]) for triplo in caminho]
                    melhorCaminho = [(self.name,self.ipRP)] + melhorCaminho[::-1]
        print("[STREAM UDP] O melhor caminho é: " , melhorCaminho)
        print("[STREAM UDP] Latência: ", latencia)
        return melhorCaminho
    

    def calculaLatencia(self,caminho):
        latencia = 0.0
        for _, _, tempo in caminho:
            latencia += tempo
        return latencia

    # pode haver nodos repetidos
    def addNodoAtivo(self,nomeVideo,nodo):
        if nomeVideo in self.nodosAtivos:
            self.nodosAtivos[nomeVideo].append(nodo)
        else:
            self.nodosAtivos[nomeVideo] = [nodo]

    # Adiciona ao dicionário para quem está a transmitir o nome do vídeo e o nodo
    def addATransmitir(self,nomeVideo,tuploVizinho):
        if nomeVideo in self.aTransmitir:
            self.aTransmitir[nomeVideo].append(tuploVizinho)
            if tuploVizinho not in self.aTransmitir[nomeVideo] :
                print("[STREAM UDP] Estou a transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
                print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)
        else:
            self.aTransmitir[nomeVideo] = [tuploVizinho]
            print("[STREAM UDP] Estou a transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
            print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)



    def rmATransmitir(self,nomeVideo,tuploVizinho):
        self.aTransmitir[nomeVideo].remove(tuploVizinho)
        if tuploVizinho not in self.aTransmitir[nomeVideo]:
            print("[STREAM UDP] Parei de transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
            print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)


    def addClienteAtivo(self,nomeVideo,nomeCliente,caminho):
        tuplo = (nomeCliente,nomeVideo)
        self.clientesAtivos[tuplo] = caminho

    def getClientesAtivos(self):
        return self.clientesAtivos

    def getATransmitir(self):
        return self.aTransmitir
    
    def removeClienteAtivo(self,nomeCliente,nomeVideo):
        tuplo = (nomeCliente,nomeVideo)
        self.clientesAtivos.pop(tuplo)
    
    def removeNodoAtivo(self,nomeVideo,tuplo):
        self.nodosAtivos[nomeVideo].remove(tuplo)

    def printControlUDP(self):
        print("[CONTROL UDP]")
        print("{Videos Disponíveis}: ", self.videos)
        print("{Nodos Ativos}: ", self.nodosAtivos)
        print("{Clientes Ativos}", self.clientesAtivos)
        print("--------------------")





rp = RP()