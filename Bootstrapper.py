import socket, sys
from TCPBootstrapper import TCPBootstrapper
from TCPReceiver import TCPReceiver
from UDPReceiver import UDPReceiver

# Como inciar o Bootstrapper: Bootstrapper.py 1 [ficheiroBootstrapper] [portaBootstrapper]

class Bootstrapper:

    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.file = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.info = {}
        self.nodos = {}
        self.vizinhos = []
        self.IpRP = ""
        self.aTransmitir = {}
        

        # Atualiza o ficheiro info e o nodos
        self.parserConfig(self.file)

        # Atualiza os seus vizinhos
        self.vizinhos = self.getVizinhosbyName(self.name)


        # Coloca TCP Bootstrapper á escuta
        serverTCPBootstrapper = TCPBootstrapper(self.portaBootstrapper,self)
        serverTCPBootstrapper.start()


        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"","","")
        serverTCP.start()

        # Colocar UDP à escuta
        serverUDP = UDPReceiver(self)
        serverUDP.start()







    # Parse do ficheiro de configuração
    def parserConfig(self,file):
        f = open(file, 'r')
        for line in f:
            if(line[0] != '#'):
                partes = line.strip().split(':')
                ip = tuple(map(str, partes[0][1:-1].split(',')))
                vizinhos = partes[1].split(';')
                self.info[ip] = [tuple(map(str, v[1:-1].split(','))) for v in vizinhos]
                if (ip[0][0] == "n"):   
                    self.nodos[ip[0]] = "0" 

    # Retorna os vizinhos através do nome 
    def getVizinhosbyName(self,nome):
        for chave, listavalores in self.info.items():
            if chave[0]==nome:
                return listavalores


    
    def setNodoOFF(self,nodo):
        self.nodos[nodo] = "0"
        print("O nodo " + nodo + " está desligado.")

    def setNodoON(self,nodo,ip):
        self.nodos[nodo] = ip

    def getNodos(self):
        return self.nodos
    
    def getIpRP(self):
        return self.IpRP
    
    def setIpRP(self,ip):
        self.IpRP = ip

    def getIPbyName(self,name):
        for nome, ip in self.info.keys():
            if name == nome:
                return ip

    def setVizinhos(self,vizinhos):
        self.vizinhos = vizinhos
    
    def getVizinhos(self):
        return self.vizinhos

    def getType(self):
        return self.type
    
    def getNome(self):
        return self.name
            
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

    def getATransmitir(self):
        return self.aTransmitir


    def rmATransmitir(self,nomeVideo,tuploVizinho):
        self.aTransmitir[nomeVideo].remove(tuploVizinho)
        if tuploVizinho not in self.aTransmitir[nomeVideo]:
            print("[STREAM UDP] Parei de transmitir o vídeo " + nomeVideo + " para o nodo " + tuploVizinho[0])
            print("[STREAM UDP] {A Transmitir}:" , self.aTransmitir)
            


bootstrapper = Bootstrapper()