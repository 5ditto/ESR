import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	

    def __init__(self):
        self.header  = bytearray(HEADER_SIZE)
        self.payload = None

		
    def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
        """Encode the RTP packet with header fields and payload."""
        timestamp = int(time())
        header = bytearray(HEADER_SIZE)
        header[0] = (version << 6) & 0xC0
        header[0] |= ((padding & 0x01) << 5) | ((extension & 0x01) << 4) | (cc & 0x0F)
        header[1] = ((marker & 0x01) << 7) | (pt & 0x7F)
        header[2] = (seqnum >> 8) & 0xFF
        header[3] = seqnum & 0xFF
        header[4] = (timestamp >> 24) & 0xFF
        header[5] = (timestamp >> 16) & 0xFF
        header[6] = (timestamp >> 8) & 0xFF
        header[7] = timestamp & 0xFF
        header[8] = (ssrc >> 24) & 0xFF
        header[9] = (ssrc >> 16) & 0xFF
        header[10] = (ssrc >> 8) & 0xFF
        header[11] = ssrc & 0xFF
        self.payload = payload
        self.header = header
		


    def decode(self, byteStream):
        """Decode the RTP packet."""
        self.header = bytearray(byteStream[:HEADER_SIZE])
        self.payload = byteStream[HEADER_SIZE:]
	
    def version(self):
        """Return RTP version."""
        return int(self.header[0] >> 6)
	
    def seqNum(self):
        """Return sequence (frame) number."""
        seqNum = self.header[2] << 8 | self.header[3]
        return int(seqNum)
	
    def timestamp(self):
        """Return timestamp."""
        timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
        return int(timestamp)
	
    def payloadType(self):
        """Return payload type."""
        pt = self.header[1] & 127
        return int(pt)
	
    def getPayload(self):
        """Return payload."""
        return self.payload

    def getPacket(self):
        """Return RTP packet."""
        return self.header + self.payload
    
    def printHeader(self):
        """Print RTP header information."""
        print("[RTP HEADER]")
        print(f"Version: {self.version()}")
        print(f"Sequence Number: {self.seqNum()}")
        print(f"Timestamp: {self.timestamp()}")
        print(f"Payload Type: {self.payloadType()}")
        print("--------------")
        
















# Exemplo de uso
# Supondo que você tenha os valores apropriados para PType, Framenb, Time, ID, data e data_length
# rtp_packet = RTPPacket(PType, Framenb, Time, ID, data, data_length)
