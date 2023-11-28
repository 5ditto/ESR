import queue
import threading

from Packet import Packet

class PacketQueue:
    def __init__(self,servidorTCP):
        self.packet_queue = queue.Queue()
        self.condition = threading.Condition()
        self.TCPserver = servidorTCP

        # Iniciar thread para escutar a fila de pacotes
        self.listen_thread = threading.Thread(target=self.listen_packets)
        self.listen_thread.start()

    def listen_packets(self):
        while True:
            with self.condition:
                while self.packet_queue.empty():
                    # Aguardar até que haja pacotes na fila
                    self.condition.wait()

                packet = self.packet_queue.get()
                self.process_packet(packet)


    def process_packet(self, packet):
        source = packet.getSource()
        data = packet.getData()
        self.TCPserver.adicionaVizinho(source,data)
        self.TCPserver.enviaPackets(data)


        

    def add_packet(self, packet):
        with self.condition:
            self.packet_queue.put(packet)
            # Notificar a thread de escuta que há novos pacotes
            self.condition.notify()