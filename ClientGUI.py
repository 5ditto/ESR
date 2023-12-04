import pickle
from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from TCPSender import TCPSender
from Packet import Packet

import socket, threading, os

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

class ClientGUI:
	
	# Initiation..
	def __init__(self, master,nomeCliente,ipRP,nomeVideo):
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.handler)
		self.createWidgets()
		self.port = 1234
		self.nomeCliente = nomeCliente
		self.rtpSocket = None
		self.ipRP = ipRP
		self.On = False
		self.nomeVideo = nomeVideo
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.terminar = 0
		self.openRtpPort()
		self.playMovie()
		self.frameNbr = 0
		self.isPlaying = False
		
	def createWidgets(self):
		"""Build GUI."""
		# Create Setup button
		self.setup = Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		# Create Play button		
		self.start = Button(self.master, width=20, padx=3, pady=3)
		self.start["text"] = "Play"
		self.start["command"] = self.playMovie
		self.start.grid(row=1, column=1, padx=2, pady=2)
		
		# Create Pause button			
		self.pause = Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)
		
		
		# Create a label to display the movie
		self.label = Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S, padx=5, pady=5)

	
	def setupMovie(self):
		packetVideo = Packet(self.nomeCliente,self.ipRP,9,self.nomeVideo)
		TCPSender(packetVideo,12345)
		self.On = True
		
	
	def exitClient(self):
		"""Teardown button handler."""
		self.master.destroy() # Close the gui window

		cache_file_path = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		if os.path.exists(cache_file_path):
			os.remove(cache_file_path) # Delete the cache image from video

		if self.On:
			packetExitVideo = Packet(self.nomeCliente,self.ipRP,12,self.nomeVideo)
			TCPSender(packetExitVideo,12345)
		if self.rtpSocket:
			print("Conexão Terminada.")
			self.rtpSocket.close()
	
	def pauseMovie(self):
		"""Pause button handler."""
		self.isPlaying = False

	
	def playMovie(self):
		"""Play button handler."""
		self.isPlaying = True
		# Create a new thread to listen for RTP packets
		threading.Thread(target=self.listenRtp).start()
		self.playEvent = threading.Event()
		self.playEvent.clear()
	
	def listenRtp(self):		
		"""Listen for RTP packets."""
		while True:
				data = self.rtpSocket.recv(20480)
				if data:
					packet = pickle.loads(data)

					currFrameNbr = packet.seqNum()
					print("Current Seq Num: " + str(currFrameNbr))

					if currFrameNbr > self.frameNbr: # Discard the late packet
						self.frameNbr = currFrameNbr
						if self.isPlaying:
							self.updateMovie(self.writeFrame(packet.getPayload()))

				
	
	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
		cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		file = open(cachename, "wb")
		file.write(data)
		file.close()
		
		return cachename
	
	def updateMovie(self, imageFile):
		"""Update the image file as video frame in the GUI."""
		photo = ImageTk.PhotoImage(Image.open(imageFile))
		self.label.configure(image = photo, height=288) 
		self.label.image = photo
		
	



	def openRtpPort(self):
		"""Open RTP socket binded to a specified port."""
		
    	# Verifique se o socket já existe e, se sim, feche-o
		if hasattr(self, 'rtpSocket') and self.rtpSocket:
			self.rtpSocket.close()

		self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		try:
        # Permita a reutilização do endereço mesmo que ainda esteja no estado TIME_WAIT
			self.rtpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.rtpSocket.bind(('', self.port))

		except Exception as e:
			messagebox.showwarning('Unable to Bind', 'Unable to bind PORT=%d: %s' % (self.port, str(e)))
			self.rtpSocket = None


	def handler(self):
		"""Handler on explicitly closing the GUI window."""
		self.pauseMovie()
		if messagebox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.exitClient()
		else: # When the user presses cancel, resume playing.
			self.playMovie()
