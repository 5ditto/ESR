import random


class Packet:

    def __init__(self,source,destination,type,data):
        self.id = random.randint(1,100000) 
        self.source = source
        self.destination = destination
        self.type = type
        self.data = data

    def getID(self):
        return self.id

    def getSource(self):
        return self.source
    
    def getDestination(self):
        return self.destination
    
    def getType(self):
        return self.type
    
    def getData(self):
        return self.data
    
    def printReceived(self):
        msg = "\n[PACKET RCVD] "
        msg += "\nID: " + str(self.id)
        msg += "\nType: " + str(self.type)
        msg += "\nSource: " + self.source
        msg += "\nMSG: "

        if self.type == 1:
            msg += "Recebi pedido de vizinhos\n"

        if self.type == 2:
            msg += "Recebi vizinhos\n"
        
        if self.type == 3:
            msg += "Ping do Bootstrapper\n"
        
        if self.type == 4:
            msg += "Recebi pedido de Fload\n"
        
        if self.type == 5:
            msg += "Recebi IP do RP\n"
        
        if self.type == 6:
            msg += "Recebi os vídeos que o Servidor possui\n"
        
        if self.type == 7:
            msg += "Recebi pedido de vídeo do Cliente\n"
        
        if self.type == 8:
            msg += "Recebi os vídeos disponíveis\n"
        
        if self.type == 9:
            msg += "Recebi nome do video selecionado\n"
        
        if self.type == 10:
            msg += "Recebi nome do vídeo a transmitir e para onde devo transmitir\n"
            
        msg += str(self.data)
        msg += "\n--------------"
        
        print(msg)
        


    def printSent(self):
        msg = "\n[PACKT SENT] "
        msg += "\nID: " + str(self.id)
        msg += "\nType: " + str(self.type)
        msg += "\nDestination: " + self.destination
        msg += "\nMSG: " 

        if self.type == 1:
            msg += "Enviei pedido de vizinhos\n"

        if self.type == 2:
            msg += "Enviei vizinhos\n"

        if self.type == 3:
            msg += "Enviei ping\n"
        
        if self.type == 4:
            msg += "Envei Fload\n"


        if self.type == 5:
            msg += "Enviei IP do RP\n"
        
        if self.type == 6:
            msg += "Enviei vídeos que possuo\n"
        
        if self.type == 7:
            msg += "Enviei pedido de vídeo\n"
        
        if self.type == 8:
            msg += "Enviei vídeos disponíveis\n"
        
        if self.type == 9:
            msg += "Enviei nome do vídeo selecionado\n"
        
        if self.type == 10:
            msg += "Enviei o nome do vídeo a transmitir e para onde\n"


        msg += str(self.data)
        msg += "\n--------------"
        
        print(msg)
