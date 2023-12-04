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
                time = self.packet.getTime()
                self.adicionaVizinho(source, data, time)
                cliente = data[0][0]
                self.rp.adicionaCaminho(cliente,data)


            if self.routerType == 1 or self.routerType == 0:
                self.packet.printReceived()
                source = self.packet.getSource()
                data = self.packet.getData()
                time = self.packet.getTime()
                self.adicionaVizinho(source,data,time)
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
            self.rp.addVideos((source,self.ipOrigem),videos)

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
            nomeVideo = self.packet.getData()
            self.rp.printArvore()
            melhorCaminho = self.rp.melhorCaminho(nomeCliente,nomeVideo)
            videosAtivos = list(self.rp.getNodosAtivos().keys())
            if nomeVideo not in videosAtivos:
                self.enviaPacketRPtoServidor(nomeVideo)
            self.enviaPacketsRP(melhorCaminho,nomeVideo,nomeCliente)



        # Quando cada nodo recebe o titulo do video e o nodo para quem deve enviar
        elif self.packetType == 10:
            self.packet.printReceived()
            data = self.packet.getData()
            self.router.addATransmitir(data[0],data[1])

        # Quando o servidor recebe uma mensagem para transmitir o vídeo
        elif self.packetType == 11:
            self.packet.printReceived()
            data = self.packet.getData()
            self.router.addVideosATransmitir(data)

        # Quando o cliente manda a dizer que nao quer mais video
        elif self.packetType == 12:
            self.packet.printReceived()
            nomeCliente = self.packet.getSource()
            nomeVideo = self.packet.getData()
            self.terminaVideo(nomeCliente,nomeVideo)
            self.router.printControlUDP()

            
        # Remover do dic aTransmitir
        elif self.packetType == 13:
            self.packet.printReceived()
            data = self.packet.getData()
            nomeVideo = data[0]
            nodo = data[1]
            self.router.rmATransmitir(nomeVideo,nodo)

        # Parar de transmitir o vídeo
        elif self.packetType == 14:
            self.packet.printReceived()
            data = self.packet.getData()
            self.router.rmATransmitir(data)


            





    # Método para adicionar o vizinho que lhe enviou o packet ao caminho
    def adicionaVizinho(self,nodo,data,timePacket):
        for vizinho in self.router.getVizinhos():
            if vizinho[0] == nodo:
                tuplo = vizinho
                break
        tempoAtual = time.time()
        triplo = (tuplo[0],tuplo[1],round((tempoAtual-timePacket)*1000,2))
        data.append(triplo)


    # Método para enviar dados aos seus vizinhos ao fazer fload
    def enviaPackets(self,data):
        caminho = [(nome, ip) for nome, ip, _ in data]

        for vizinho in self.router.getVizinhos():
            if vizinho not in caminho:
                packet = Packet(self.name,vizinho[1],4,data)
                time.sleep(1)   # apenas para ver o funcionamento dos packets (senão envia tudo de uma vez)
                TCPSender(packet,12345)


    # Manda o pacote com o nome do video e o vizinho para quem deve enviar
    def enviaPacketsRP(self,caminho,nomeVideo,nomeCliente):
        self.rp.addClienteAtivo(nomeVideo,nomeCliente,caminho)
        for i, nodo in enumerate(caminho[:-1]):
            data = (nomeVideo,caminho[i+1])
            packet = Packet("RP",nodo[1],10,data)
            TCPSender(packet,12345)
            self.rp.addNodoAtivo(nomeVideo,nodo)
        self.router.printControlUDP()


    def enviaPacketRPtoServidor(self,nomeVideo):
        videos = self.router.getVideos()
        nodo = videos[nomeVideo]
        packet = Packet("RP",nodo[1],11,nomeVideo)
        TCPSender(packet,12345)





    def terminaVideo(self,nomeCliente,nomeVideo):
        # eliminar dos clientes ativos 
        # para o caminho dos clientes ativos enviar um packet para removerem dos aTransmitr
        # remover dos nodos ativos uma entrada e caso depois o array fique vazio temos que avisar o servidor

        clientesAtivos = self.router.getClientesAtivos()
        listaNodos = clientesAtivos[(nomeCliente,nomeVideo)]
        for i, nodo in enumerate(listaNodos):
            if i + 1 < len(listaNodos):
                tuplo = (nomeVideo,listaNodos[i+1])
                packet = Packet("RP",nodo[1],13,tuplo)
                TCPSender(packet,12345)
                self.router.removeNodoAtivo(nomeVideo,nodo)
        
        if (not self.router.getNodosAtivos()[nomeVideo]):
            self.router.getNodosAtivos().pop(nomeVideo)
            server = self.router.getVideos()[nomeVideo]
            packetServer = Packet("RP",server[1],14,nomeVideo)
            TCPSender(packetServer,12345)


        self.router.removeClienteAtivo(nomeCliente,nomeVideo)
        





