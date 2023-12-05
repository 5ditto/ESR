import pickle
import socket, sys,threading
import time


from TCPSender import TCPSender
from UDPReceiver import UDPReceiver
from VideoStream import VideoStream
from TCPReceiver import TCPReceiver
from Packet import Packet
from RTPpacket import RtpPacket

# Como inciar o Servidor: Server.py 4 [ipBootstrapper] [portaBootstrapper] [nomeVideo] [nomeVideo] ...


class Server:
    
    def __init__(self):
        self.name = socket.gethostname()
        self.type = int(sys.argv[1])
        self.ipBootstrapper = sys.argv[2]
        self.portaBootstrapper = sys.argv[3]
        self.videosName = sys.argv[4:]
        self.gotVizinhos = threading.Event()
        self.gotIpRP = threading.Event()
        self.vizinhos = []
        self.ipRP = ""

        self.videosATransmitir = [] 


        # Colocar TCP à escuta
        serverTCP = TCPReceiver(self,"",self,"")
        serverTCP.start()


        # Pedir vizinhos ao Bootstrapper
        packetVizinhos = Packet(self.name,self.ipBootstrapper,1,self.type)
        TCPSender(packetVizinhos,self.portaBootstrapper)
        self.gotVizinhos.wait()     # espera receber os vizinhos


        self.gotIpRP.wait()     # espera receber o Ip do RP


        # Diz ao RP quais os vídeos que tem
        packetServer = Packet(self.name, self.ipRP,6,self.videosName)
        TCPSender(packetServer,12345)


        






    

    def getIpRP(self):
        return self.ipRP
    
    def setIpRP(self,ip):
        self.ipRP = ip

    
    def setVizinhos(self,vizinhos):
        self.vizinhos = vizinhos
    
    def getVizinhos(self):
        return self.vizinhos

    def getNome(self):
        return self.name
    
    def getEventVizinhos(self):
        return self.gotVizinhos
    
    def getType(self):
        return self.type

    def getEventIpRP(self):
        return self.gotIpRP

    # Adiciona ao dicionário para quem está a transmitir o nome do vídeo e o nodo
    def addVideosATransmitir(self,nomeVideo):
        self.videosATransmitir.append(nomeVideo)
        print("[STREAM UDP] Vou transmitir este vídeo " + nomeVideo)
        print("[STREAM UDP] {Vídeos ON} ", self.videosATransmitir)

        threadUDP = SendUDPPacket(self,nomeVideo)   # Começa a transmitir o vídeo
        threadUDP.start()


    def getATransmitir(self):
        return self.videosATransmitir

    def rmATransmitir(self,nomeVideo):
        video =  self.videosATransmitir.remove(nomeVideo)
        print("[STREAM UDP] Vou parar de transmitir este vídeo " + nomeVideo)
        print("[STREAM UDP] {Vídeos ON} ", self.videosATransmitir)
        return video



class SendUDPPacket(threading.Thread):

    def __init__(self,server,videoName):
        super().__init__()
        self.server = server
        self.video = VideoStream(videoName)
        self.videoName = videoName

    def run(self):
        videosName = self.server.getATransmitir()
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        while self.videoName in videosName:
            time.sleep(0.05)
            data = self.video.nextFrame()
            if data:
                frameNumber = self.video.frameNumber()
                addr = self.server.getIpRP()
                porta = 1234
                packet = self.makeRtp(data, frameNumber, self.videoName)
                udp_socket.sendto(pickle.dumps(packet),(addr,porta))
            else:
                self.video.seek()




    def makeRtp(self, payload, frameNbr,videoName):
        
        """RTP-packetize the video data."""
        version = 2
        padding = 0
        extension = 0
        cc = 0
        marker = 0
        pt = 26 # MJPEG type
        seqnum = frameNbr
        ssrc = 0

        rtpPacket = RtpPacket(version,padding,extension,cc,seqnum,marker,pt,ssrc,videoName,payload)

        return rtpPacket





        

server = Server()