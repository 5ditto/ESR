import pickle
import socket

from Packet import Packet
from TCPSender import TCPSender

class TCPReceiver:

    def __init__(self,router):
        self.nome = router.getNome()
        self.type = router.getType()
        self.router = router

        

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        tcp.bind(('',12345))
        while 1:

            tcp.listen(1)

            c,addr = tcp.accept()

            data = c.recv(1024)
            packet = pickle.loads(data)
            packet.printReceived()



            if packet.getType() == 2:
                router.setVizinhos(packet.getData())
                self.router.getEventVizinhos().set()    # avisa que já possui vizinhos

            
            if packet.getType() == 4:

                if (self.type != "2"): # quando não é o RP a receber
                    # quando recebe pedido de fload
                    source = packet.getSource()
                    data = packet.getData()
                    self.adicionaVizinho(source,data)
                    self.enviaPackets(data)

                if (self.type == "2"): # quando é o RP
                    caminhos = []
                    source = packet.getSource()
                    data = packet.getData()
                    self.adicionaVizinho(source,data)
                    cliente = data[0][0]
                    caminho = (cliente,data[::-1])
                    caminhos.append(caminho)
                    print(caminhos)





    def adicionaVizinho(self,nodo,data):
        for vizinho in self.router.getVizinhos():
            if vizinho[0] == nodo:
                data.append(vizinho)

    def enviaPackets(self,data):
        
        for vizinho in self.router.getVizinhos():
            if vizinho not in data:
                packet = Packet(self.nome,vizinho[1],4,data)
                TCPSender(packet,12345)

                
