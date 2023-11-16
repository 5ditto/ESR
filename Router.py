import socket
import sys
import threading
from Bootstrapper import Bootstrapper 


# Caso o nodo seja Bootstrapper: Router.py 1 [ficheiroBootstrapper] [ipBootstrapper] [porta]
# Caso o nodo seja normal: Router.py 0 [ipBoostrapper] [portaBootstrapper]

class Router:

    def __init__(self):
        self.vizinhos = []
        self.nome = socket.gethostname()
        self.bootstrapper = (sys.argv[1])


        if(self.bootstrapper == "1"):
            print("Sou o Bootstrapper.")
            file = sys.argv[2]
            ip = sys.argv[3]
            porta = int(sys.argv[4])
            bootstrapper = Bootstrapper(file,porta)
            self.vizinhos = bootstrapper.getVizinhos(ip)   
            thread_bootstrapper = threading.Thread(target=bootstrapper.run)
            thread_bootstrapper.start()
        
        
        if(self.bootstrapper == "0"):
            ipBootstrapper = sys.argv[2]
            portaBootstrapper = int(sys.argv[3])
            self.getVizinhos(ipBootstrapper,portaBootstrapper)
            print(self.vizinhos)
            



    def getVizinhos(self,ipBootstrapper,porta):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((ipBootstrapper,porta)) 
        print("Conexão Estabelecida com Bootstrapper: (" + ipBootstrapper + ":" + str(porta) + ")")

        tcp.send("Vizinhos".encode('utf-8'))    #manda uma mensagem a pedir os vizinhos
        msg = tcp.recv(1024).decode('utf-8')    # recebe os vizinhos
        self.vizinhos.append(msg)
        while msg:
            msg = tcp.recv(1024).decode('utf-8')
            if msg == "0":
                break
            self.vizinhos.append(msg)
        tcp.close()
    


    def buildTree(self):
        print("OI")
        for v in self.vizinhos:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((v,2020))
            print("Conexão Estabelecida com Vizinho: (" + v + ":" + str(2020) + ")")
            tcp.send(self.nome.encode('utf-8'))
            

router = Router()
