import socket
import time
import json
class Bootstrapper:

    def __init__(self,file):
        self.info = {}
        self.nodos = {}
        self.parserConfig(file)




    # Parse do ficheiro de configuração
    def parserConfig(self,file):
        f = open(file, 'r')
        for line in f:
            if(line[0] != '#'):
                partes = line.strip().split(':')
                ip = tuple(map(str, partes[0][1:-1].split(',')))
                vizinhos = partes[1].split(';')
                self.info[ip] = [tuple(map(str, v[1:-1].split(','))) for v in vizinhos]
                if (ip[0][0] == "n"):   # temos que mudar para "O" quando usarmos a topologia normal
                    self.nodos[ip[0]] = "0" 
        #print(self.info) # dá print ao dicionario
    
    def getVizinhos(self,nome):
        for chave, listavalores in self.info.items():
            if chave[0]==nome:
                return listavalores


    
    def setNodoOFF(self,nodo):
        self.nodos[nodo] = "0"
        print("O nodo " + nodo + " está desligado.")

    def setNodoON(self,nodo,ip):
        self.nodos[nodo] = ip


    def getNodos(self):
        return self.nodos
    
            

            


