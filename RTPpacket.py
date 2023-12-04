from time import time


class RtpPacket:	

    def __init__(self,version,padding, extension, cc, seqnum, marker, pt, ssrc, videoName, payload):
        self.header  = [0] * 10
        self.header[0] = version
        self.header[1] = padding
        self.header[2] = extension
        self.header[3] = cc
        self.header[4] = seqnum
        self.header[5] = marker
        self.header[6] = pt
        self.header[7] = ssrc
        self.header[8] = int(time())
        self.header[9] = videoName
        self.payload = payload
        
	
    def seqNum(self):
        return self.header[4]

	
    def getPayload(self):
        """Return payload."""
        return self.payload
    
    def getVideoName(self):
        return self.header[9]

    def getPacket(self):
        """Return RTP packet."""
        return self

    
    def printHeader(self):
        """Print RTP header information."""
        print("[RTP HEADER]")
        print(f"Version: {self.header[0]}")
        print(f"Sequence Number: {self.header[4]}")
        print(f"Timestamp: {self.header[8]}")
        print("Video Name: " + self.header[9])
        print("--------------")
        















