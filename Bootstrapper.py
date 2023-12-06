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
        self.clientes = []
        

        # Atualiza o ficheiro info e o nodos
        self.parserConfig(self.file)

        # Atualiza os seus vizinhos
        self.vizinhos = self.getVizinhosbyName(self.name)
        meuIP = self.getIPbyName(self.name)
        self.setNodoON(self.name,meuIP)


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
                    self.nodos.setdefault(ip[0], "0")
                if len(self.info[ip]) == 1:
                    self.clientes.append(ip)

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

    def getInfo(self):
        return self.info

    def getNodos(self):
        return self.nodos


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

    def addCliente(self,cliente):
        self.clientes.append(cliente)
    
    def getClientes(self):
        return self.clientes
            
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


    def substituiVizinhos(self, nodoDown):
        if nodoDown in self.info:
            vizinhos = self.info.pop(nodoDown)
            for nodo in vizinhos:
                for nodoA in vizinhos:
                    if nodo in self.clientes and nodoA in self.clientes:
                        pass
                    elif nodo != nodoA:
                        self.info[nodo].append(nodoA)
                    
                if nodoDown in self.info[nodo]:
                    self.info[nodo].remove(nodoDown)
        
        for tuplo, vizinhosA in self.info.items():
            self.info[tuplo] = list(set(vizinhosA))
    
    def clearATransmitir(self):
        self.aTransmitir.clear()

    def setNewFile(self):
        self.clientes.clear()
        self.info.clear()
        self.file = input("Insira novo ficheiro: ")
        self.parserConfig(self.file)




bootstrapper = Bootstrapper()