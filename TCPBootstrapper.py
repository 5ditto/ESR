import pickle
import socket
import threading
import time
import pickle

from Packet import Packet
from TCPSender import TCPSender


class TCPBootstrapper:

    def __init__(self,porta,bootstrapper):
        self.porta = porta
        self.bs = bootstrapper

        # criar thread para o Bootstrapper ver os routers ativos
        threadVerificaRouters = threading.Thread(target=self.verificaLigacao)
        threadVerificaRouters.start()
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        tcp.bind(('',self.porta))

        while 1:

            tcp.listen(1)
            c,addr = tcp.accept()

            data = c.recv(1024)
            packet = pickle.loads(data)
            packet.printReceived()


            if packet.getType() == 1:
                nomeNodo = packet.getData()
                ipNodo = addr[0]
                self.bs.setNodoON(nomeNodo,ipNodo)      # quando um router se liga ao Bootstrapper adiciona-mos aos nodos ativos
                time.sleep(0.5)
                data = self.bs.getVizinhos(nomeNodo)
                packet = Packet("Bootstrapper",ipNodo,2,data)
                self.send(packet,12345)


    


    def send(self,packet, porta):
        packet.printSent()
        ipDest = packet.getDestination()
        
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((ipDest,porta))
            serializedPack = pickle.dumps(packet)
            tcp.sendall(serializedPack)
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar a " + ipDest)
            if packet.getType() == 3:
                self.bs.setNodoOFF(packet.getData())            # colocar o router desligado
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            tcp.close()

    
    def verificaLigacao(self):
        
        while 1:
            
            nodos = self.bs.getNodos()

            for nodo, ip in nodos.items():
                if ip != "0":               # quer dizer que o nodo está ativo
                    packet = Packet("Bootstrapper",ip,3,nodo)
                    self.send(packet,12345)
            time.sleep(60)                  # 60 em 60 segundos verifica se os routers estão ativos



