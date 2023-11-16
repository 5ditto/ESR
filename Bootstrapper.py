
import socket
import time

class Bootstrapper:

    def __init__(self,file,porta):
        self.info = {}
        self.parserConfig(file)
        self.porta = porta


    # Parse do ficheiro de configuração
    # Formato - IP_Nodo:IP_Vizinho1;IP_Vizinho2...
    def parserConfig(self,file):
        f = open(file, 'r')
        for line in f:
            if(line[0] != '#'):
                partes = line.strip().split(':')
                ip = partes[0]
                vizinhos = partes[1].split(',')
                self.info[ip] = vizinhos
        #print(self.info) # dá print ao dicionario com os ip's

    
    def getVizinhos(self,ip):
        return self.info[ip]




    def run(self):

        # Cria um Socket TCP
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Liga o socket ao endereço IP e à porta especificados
        tcp.bind(('',self.porta))
        
        while 1:        

            tcp.listen(1)

            c, addr = tcp.accept()
            if (c.recv(1024).decode('utf-8')) == "Vizinhos":
                print("Conexão estabelecida com " + addr[0] + " pela porta " + str(addr[1]))
                vizinhos = self.getVizinhos(addr[0])

            for v in vizinhos:
               c.send(v.encode('utf-8'))
               time.sleep(0.1)
            msg = "0"
            c.send(msg.encode('utf-8'))

            

            


