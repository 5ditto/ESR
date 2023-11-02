import sys
import socket
import threading

class RP:
    def __init__(self):
        self.ficheiroConfig = sys.argv[1]
        self.bootstraper = {}
        self.parserConfig()
        #threading.Thread(target=self.conexaoTCP, args=()).start() 
    
    
    # Parse do ficheiro de configuração
    # Formato - IP_Nodo:IP_Vizinho1;IP_Vizinho2...
    def parserConfig(self):
        f = open(self.ficheiroConfig, 'r')
        for line in f:
            if(line[0] != '#'):
                partes = line.strip().split(':')
                ip = partes[0]
                vizinhos = partes[1].split(';')
                self.bootstraper[ip] = vizinhos
                print(self.bootstraper)

    
rp = RP()