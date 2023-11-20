import pickle
import socket
from Packet import Packet

class TCPSender:

    def __init__(self,packet,porta):
        self.packet = packet
        self.IPDest = packet.getDestination()
        self.porta = porta
        self.packet.printSent()

        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((self.IPDest,self.porta))
            serializedPack = pickle.dumps(self.packet)
            tcp.sendall(serializedPack)
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar a " + self.IPDest)
        except Exception as e:
            print(f"Erro inesperado: {e}")
        finally:
            tcp.close()

        
