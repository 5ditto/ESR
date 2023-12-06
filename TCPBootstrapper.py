import pickle, socket, threading, time

from Packet import Packet


class TCPBootstrapper(threading.Thread):

    def __init__(self,porta,bootstrapper):
        super().__init__()
        self.porta = int(porta)
        self.bs = bootstrapper



    def run(self):

        # criar thread para o Bootstrapper ver os routers ativos
        threadVerificaRouters = threading.Thread(target=self.verificaLigacao)
        threadVerificaRouters.start()


        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tcp.bind(('',self.porta))
        tcp.listen(1)

        while True:
            c,addr = tcp.accept()

            data = c.recv(1024)
            packet = pickle.loads(data)
            packet.printReceived()

            handler_thread = PacketHandlerBootstrapper(12345,self.bs,packet)
            handler_thread.start()





    # Para verificar se os routers estão ativos
    def verificaLigacao(self):
        # podia fazer ao receber o pedido dos vizinhos mandar o tipo e assim apenas fazia ping aos routers e nao aos clientes
        while 1:
            stringPing = "[BOOTSTRAPPER CONTROL] Mandei ping para "
            for nome, ip in self.bs.getNodos().items():
                if ip != "0":
                    stringPing += nome + " "
            print(stringPing)

            nodos = self.bs.getNodos()

            for nodo, ip in nodos.items():
                if ip != "0":               # quer dizer que o nodo está ativo
                    packet = Packet("Bootstrapper",ip,3,nodo)
                    self.sendPing(packet,12345)
            time.sleep(20)                  # 60 em 60 segundos verifica se os routers estão ativos




    def sendPing(self,packet, porta):
        #packet.printSent()
        ipDest = packet.getDestination()
        
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((ipDest,porta))
            serializedPack = pickle.dumps(packet)
            tcp.sendall(serializedPack)
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar a " + ipDest)
            self.bs.setNodoOFF(packet.getData())           # colocar o router desligado
            ip = self.bs.getIPbyName(packet.getData())
            
            self.bs.substituiVizinhos((packet.getData(),ip))

             # enviar ao RP para limpar a árvore
            packetRP = Packet("Bootstrapper",self.bs.getIpRP(),15,"ERROR")
            self.send(packetRP,12345)

            #enviar novos vizinhos
            for nome, ip in self.bs.getNodos().items():
                if ip != "0":
                    vizinhos = self.bs.getVizinhosbyName(nome)
                    packetVizinho = Packet("Bootstrapper",ip,2,vizinhos)
                    self.send(packetVizinho,12345)

                    # limpar o campo ATransmitir
                    packetATransmitir = Packet("Bootstrapper",ip,17,"CLEAR")
                    self.send(packetATransmitir,12345)
             
            
             # enviar aos clientes para fazerem fload
            for nome,ip in self.bs.getClientes():
                packetCliente = Packet("Bootstrapper",ip,16,"FLOAD")
                self.send(packetCliente,12345)


        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            tcp.close()




    
    def send(self,packet, porta):
        #packet.printSent()
        packet.printSentShort()
        ipDest = packet.getDestination()
        
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((ipDest,porta))
            serializedPack = pickle.dumps(packet)
            tcp.sendall(serializedPack)
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar a " + ipDest)
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            tcp.close()



class PacketHandlerBootstrapper(threading.Thread):

    def __init__(self, porta, bootstrapper,packet):
        super().__init__()
        self.porta = porta
        self.bs = bootstrapper
        self.packet = packet
        self.packetType = self.packet.getType()



    def run(self):

            # Recebe a pedir Vizinhos
            if self.packetType == 1:

                nomeNodo = self.packet.getSource()
                ipNodo = self.bs.getIPbyName(nomeNodo)
                typeSource = self.packet.getData()
                if ipNodo:
                    self.bs.setNodoON(nomeNodo,ipNodo)      # quando um router se liga ao Bootstrapper adiciona-mos aos nodos ativos
                vizinhos = self.bs.getVizinhosbyName(nomeNodo)
                if not vizinhos:
                    self.novoCliente(nomeNodo)
                else:
                    packet = Packet("Bootstrapper",ipNodo,2,vizinhos)
                    time.sleep(1)
                    self.send(packet,12345)


                # Quando é um cliente ou servidor manda o IP do RP
                if typeSource == 3 or typeSource == 4:
                    packetipRP = Packet("Bootstrapper",ipNodo,5,self.bs.getIpRP())
                    self.send(packetipRP,12345)

                # Quando é o RP guarda o Ip do RP
                if typeSource == 2:
                    ipRP = self.bs.getIPbyName(nomeNodo)
                    self.bs.setIpRP(ipRP)
                    packetipRP = Packet("Bootstrapper",ipRP,5,ipRP)
                    self.send(packetipRP,12345)





    def send(self,packet, porta):
        #packet.printSent()
        packet.printSentShort()
        ipDest = packet.getDestination()
        
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((ipDest,porta))
            serializedPack = pickle.dumps(packet)
            tcp.sendall(serializedPack)
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar a " + ipDest)
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            tcp.close()


    
    def novoCliente(self,nome):
        self.bs.setNewFile()
        ip = self.bs.getIPbyName(nome)
        self.bs.setNodoON(nome,ip)

        # enviar ao RP para limpar a árvore
        packetRP = Packet("Bootstrapper",self.bs.getIpRP(),15,"ERROR")
        self.send(packetRP,12345)

        for nodo, ip in self.bs.getNodos().items():
            if ip != "0":
                vizinhos = self.bs.getVizinhosbyName(nodo)
                packetVizinho = Packet("Bootstrapper",ip,2,vizinhos)
                self.send(packetVizinho,12345)

                # limpar o campo ATransmitir
                packetATransmitir = Packet("Bootstrapper",ip,17,"CLEAR")
                self.send(packetATransmitir,12345)

         # enviar aos clientes para fazerem fload
        for nome,ip in self.bs.getClientes():
            packetCliente = Packet("Bootstrapper",ip,16,"FLOAD")
            self.send(packetCliente,12345)








