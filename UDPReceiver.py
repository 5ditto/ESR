import threading, socket


class UDPReceiver(threading.Thread):

    def __init__(self):
        super().__init__()
        pass


    def run(self):


        UDPServerSocket = socket.socket(family=socket.AF_INET, type = socket.SOCK_DGRAM)
        UDPServerSocket.bind(('', 1234))

        while True:
            bytesAdressPair = UDPServerSocket.recvfrom(1024)
            # tratar do pacote que recebeu (provavelmente enviar para os vizinhos)
            # criar outra thread para tratar cada pacote RTP




