import pickle, socket, threading, time

from Packet import Packet
from TCPSender import TCPSender


class TCPReceiver(threading.Thread):

    def __init__(self,router,rp,servidor,cliente):
        super().__init__()
        self.router = router
        self.rp = rp
        self.server = servidor
        self.client = cliente

    def run(self):

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tcp.bind(('',12345))
        tcp.listen(1)

        while True:
            c, addr = tcp.accept()

            data = c.recv(1024)
            packet = pickle.loads(data)

            # Criar uma thread para tratar o pacote
            handler_thread = PacketHandlerThread(self.router, self.rp, self.server, self.client, packet)
            handler_thread.start()
                







class PacketHandlerThread(threading.Thread):
    def __init__(self, router, rp, servidor, cliente, packet):
        super().__init__()
        self.router = router
        self.name = router.getNome()
        self.rp = rp
        self.server = servidor
        self.client = cliente
        self.packet = packet
        self.routerType = router.getType()
        self.packetType = packet.getType()


    def run(self):


        if self.packetType == 2:
            self.packet.printReceived()
            self.router.setVizinhos(self.packet.getData())
            self.router.getEventVizinhos().set()  # avisa que já possui vizinhos

        # Quando recebe packet de fload
        elif self.packetType == 4:

            # Quando é o RP
            if self.routerType == "2":
                self.packet.printReceived()
                source = self.packet.getSource()
                data = self.packet.getData()
                self.adicionaVizinho(source, data)
                cliente = data[0][0]
                caminho = (cliente, data[::-1])
                self.rp.adicionaCaminho(caminho)


            if self.routerType == "1" or self.routerType == "0":
                self.packet.printReceived()
                source = self.packet.getSource()
                data = self.packet.getData()
                self.adicionaVizinho(source,data)
                self.enviaPackets(data)

        
        # Quando recebe o packet do IP RP
        elif self.packetType == 7:
            
            # Apenas o Servidor e o Cliente recebem:
            if self.routerType == "4" and self.routerType == "3":
                self.packet.printReceived()
                ipRP = self.packet.getData()
                self.server.setIpRP(ipRP)






    # Método para adicionar o vizinho que lhe enviou o packet ao caminho
    def adicionaVizinho(self,nodo,data):
        for vizinho in self.router.getVizinhos():
            if vizinho[0] == nodo:
                data.append(vizinho)


    # Método para enviar dados aos seus vizinhos ao fazer fload
    def enviaPackets(self,data):
        
        for vizinho in self.router.getVizinhos():
            if vizinho not in data:
                packet = Packet(self.name,vizinho[1],4,data)
                time.sleep(1)   # apenas para ver o funcionamento dos packets (senão envia tudo de uma vez)
                TCPSender(packet,12345)








        





