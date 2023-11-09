import socket
import sys
from Bootstrapper import Bootstrapper 


class Router:

    def __init__(self):
        host_name = socket.gethostname()
        self.ip = socket.gethostbyname(host_name)
        self.vizinhos = []


        # Caso este Router seja Bootstrapper tem que passar como parametro: 1
        self.bootstrapper = int(sys.argv[1])
        print(self.ip)
        if(self.bootstrapper == 1):
            print("Sou o Bootstrapper.")
            file = sys.argv[2]
            bootstrapper = Bootstrapper(file)
            self.vizinhos = bootstrapper.getVizinhos(self.ip)  
        
        
        else:
            ipBootstrapper = sys.argv[1]
            self.getVizinhos(ipBootstrapper)


    def getVizinhos(self,ipBootstrapper):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((ipBootstrapper,2020)) # PORTA MANUAL TEMOS QUE MUDAR 
        print("Conexão Estabelecida com Bootstrapper: (" + ipBootstrapper + ":" + str(2020) + ")")

        tcp.send(self.ip.encode('utf-8'))
        msg = tcp.recv(1024).decode('utf-8')
        self.vizinhos.append(msg)
        while msg:
            msg = tcp.recv(1024).decode('utf-8')
            self.vizinhos.append(msg)
        tcp.close()

            

router = Router()
