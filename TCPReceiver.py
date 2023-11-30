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
            handler_thread = PacketHandlerThread(self.router, self.rp, self.server, self.client, packet, addr[0])
            handler_thread.start()
                







class PacketHandlerThread(threading.Thread):
    def __init__(self, router, rp, servidor, cliente, packet, addr):
        super().__init__()
        self.router = router
        self.name = router.getNome()
        self.rp = rp
        self.server = servidor
        self.client = cliente
        self.packet = packet
        self.routerType = router.getType()
        self.packetType = packet.getType()
        self.ipOrigem = addr

    def run(self):


        if self.packetType == 2:
            self.packet.printReceived()
            self.router.setVizinhos(self.packet.getData())
            self.router.getEventVizinhos().set()  # avisa que já possui vizinhos

        # Quando recebe packet de fload
        elif self.packetType == 4:

            # Quando é o RP
            if self.routerType == 2:
                self.packet.printReceived()
                source = self.packet.getSource()
                data = self.packet.getData()
                self.adicionaVizinho(source, data)
                cliente = data[0][0]
                caminho = (cliente, data)
                self.rp.adicionaCaminho(caminho)


            if self.routerType == 1 or self.routerType == 0:
                self.packet.printReceived()
                source = self.packet.getSource()
                data = self.packet.getData()
                self.adicionaVizinho(source,data)
                self.enviaPackets(data)

        
        # Quando recebe o packet do IP RP
        elif self.packetType == 5:
            self.packet.printReceived()
            ipRP = self.packet.getData()
            self.router.setIpRP(ipRP)
            self.router.getEventIpRP().set()

        # Quando o RP recebe o packet do Servidor a dizer quais vídeos ele possui
        elif self.packetType == 6:
            self.packet.printReceived()
            source = self.packet.getSource()
            videos = self.packet.getData()
            self.rp.addServidor(source,videos)

        # Quando o cliente pede um vídeo ao RP
        elif self.packetType == 7:
            self.packet.printReceived()
            data = self.router.getVideosDisponiveis()
            packetVideos = Packet(self.rp.getNome(),self.ipOrigem,8,data)
            TCPSender(packetVideos,12345)

        # Quando o cliente recebe os vídeos disponíveis:
        elif self.packetType == 8:
            self.packet.printReceived()
            videosDisponiveis = self.packet.getData()
            self.client.setVideosDisponiveis(videosDisponiveis)
            self.client.getEventVideosDisponiveis().set()
        
        # Quando o RP recebe o vídeo que o cliente pretende ver
        elif self.packetType == 9:
            self.packet.printReceived()
            nomeCliente = self.packet.getSource()
            videoCliente = self.packet.getData()
            self.rp.printArvore()
            melhorCaminho = self.rp.melhorCaminho(nomeCliente,videoCliente)
            self.enviaPacketsRP(melhorCaminho,videoCliente)
        
        # Quando cada nodo recebe o titulo do video e o nodo para quem deve enviar
        elif self.packetType == 10:
            self.packet.printReceived()
            data = self.packet.getData()
            self.router.addATransmitir(data[0],data[1])







            





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


    # Manda o pacote com o nome do video e o vizinho para quem deve enviar
    def enviaPacketsRP(self,caminho,nomeVideo):
        for i, nodo in enumerate(caminho[:-1]):
            data = (nomeVideo,caminho[i+1])
            packet = Packet("RP",nodo[1],10,data)
            TCPSender(packet,12345)








        





