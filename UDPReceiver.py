import pickle
import threading, socket
from RTPpacket import RtpPacket 


class UDPReceiver(threading.Thread):

    def __init__(self,router):
        super().__init__()
        self.router = router 


    def run(self):


        UDPServerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
        UDPServerSocket.bind(('', 1234))

        while True:
            packet, addr = UDPServerSocket.recvfrom(22528)
            # tratar do pacote que recebeu (provavelmente enviar para os vizinhos)
            # criar outra thread para tratar cada pacote RTP

            handler_thread = PacketHandlerThread(self.router,packet)
            handler_thread.start()


class PacketHandlerThread(threading.Thread):
    def __init__(self, router,packet):
        super().__init__()
        self.router = router
        self.packet = pickle.loads(packet)
    # Decodificando o pacote RTP
        self.routerType = router.getType()
        self.videoName = self.packet.getVideoName()




    def run(self):

        videosON = self.router.getATransmitir()
        for nodo in videosON[self.videoName]:
            self.enviarPacketVideo(nodo[1])

    

    def enviarPacketVideo(self,ip):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(pickle.dumps(self.packet), (ip, 1234))
        udp_socket.close()







    





            


