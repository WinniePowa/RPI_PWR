#!/usr/bin/python
import os,sys,time
import socket
from multiprocessing import Queue
import multiprocessing
from ipClass import tcpClient
from threading import Thread, RLock, Lock

class teranex():
	def __init__(self,name,pipeE,pipeR):
		self.addr=""
		self.port = 0
		self.name = name
		self.connected = False
		self.isActif = False
		self.red = 0
		self.blue = 0
		self.green = 0
		self.black = 0
		self.gain = 0
		self.sharp = 0
		self.sat = 0
		self.hue = 0
		self.by = 0
		self.ry = 0
		self.lumaH = 0
		self.lumaL = 0
		self.chromaH = 0
		self.chromaL = 0
		self.timerPing = 0
		self.timerDeconnecter = 0

		self.name = name
		self.pipeE = pipeE
		self.pipeR = pipeR
		self.pipeESocket = Queue()
		self.pipeRSocket = Queue()
		self.ipSocket = tcpClient(self.name,self.pipeESocket,self.pipeRSocket)


	def sendAllData(self):
		if self.isActif :
			self.pipeR.put([2,[self.red,
				self.green,
				self.blue,
				self.black,
				self.gain,
				self.sharp,
				self.hue,
				self.sat,
				self.ry,
				self.by,
				self.connected]])
	def checkActif(self):
		print("Acitf is : ",self.isActif)
	def setActif(self,value):
		print("Set actif Fonction ")
		if value == 1 :
			self.isActif = True
		else :
			self.isActif = False
		print("Set actif Fonction ",self.isActif)

	def closeConnection(self):
		self.ipSocket.closeConnection()

	def connection(self,ipaddr,port):
		print("Try connection")
		self.addr = ipaddr
		self.port = port
		self.ipSocket.tryConnection(self.addr,self.port)
		if self.ipSocket.isConnected() :
			print("Connecter ! ",self.addr)
			self.connected = True
			self.timerPing = time.time()
			self.timerDeconnecter  = time.time()
			self.pipeR.put([1,10,self.connected])
		else :
			self.connected = False
			print("PAS BON DU TOUUUTTT  !")
		
	def send(self,item,value):
		if(self.connected):
			if item == 0 : #red
				print("Send Red !")
				status = 'VIDEO ADJUST:\n'
				tmp = 'Red: '+str(self.red+value)+'\n'
				self.ipSocket.sendToSocket(status,tmp)
			elif  item == 1 :
				status = 'VIDEO ADJUST:\n'
				tmp = 'Green: '+str(self.green+value)+'\n'
				self.ipSocket.sendToSocket(status,tmp)
			elif  item == 2 :
				status = 'VIDEO ADJUST:\n'
				tmp = 'Blue: '+str(self.blue+value)+'\n'
				self.ipSocket.sendToSocket(status,tmp)

			

	def checkSendPipe(self):
		if not self.pipeE.empty(): # check info a envoyer
			emit = self.pipeE.get()
			if emit[0]== 0 :
				if emit[1] == self.name :
					self.send(emit[2],emit[3])	
			if emit[0] == -1 : # change Actif statut
				self.isActif = emit[1]	
				if  emit[1] == 1:
					self.sendAllData()
					#print("Send All from ",self.name)
			elif emit[0] == 1 : # send data from encoder to teranex
				#print("send Data !")
				self.send(emit[1],emit[2])
			elif emit[0] == 2 : # test connection
				self.connection(emit[1],9800)

	def run(self):
		while 1 :
			self.checkSendPipe() # send data to tcp
			if self.connected and time.time()-self.timerPing > 10 :
				print("PING !")
				self.send(0,0)
				self.timerPing = time.time()
				
			if self.connected and time.time()-self.timerDeconnecter > 60 :
				print("Error Deco timer > 60 sec")
				self.timerDeconnecter = time.time()
			if not self.pipeRSocket.empty() :
				data = self.pipeRSocket.get()
				dataStr = str(data[0].decode())
				self.timerDeconnecter = time.time()
				self.timerPing = time.time()
				try :
					if len(dataStr) < 20 : # update normale, pas memoire ou pas Init
						#print(data)
						if 'Red:' in dataStr:
							tmp = dataStr.split(" ")
							self.red = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,0,self.red])
							print ("Red :",self.red)
						elif 'Green: ' in dataStr :
							tmp = dataStr.split(" ")
							self.green = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,1,self.green])
						elif 'Blue: ' in dataStr :
							tmp = dataStr.split(" ")
							self.blue = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,2,self.blue])
						elif 'Black: ' in dataStr :
							tmp = dataStr.split(" ")
							self.black = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,3,self.black])
						elif 'Gain: ' in dataStr :
							tmp = dataStr.split(" ")
							self.gain = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,4,self.gain])
						elif 'Sharp: ' in dataStr :
							tmp = dataStr.split(" ")
							self.sharp = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,5,self.sharp])
						elif 'Hue: ' in dataStr :
							tmp = dataStr.split(" ")
							self.hue = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,6,self.hue])
						elif 'Saturation: ' in dataStr :
							tmp = dataStr.split(" ")
							self.sat = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,7,self.sat])
						elif 'RY: ' in dataStr :
							tmp = dataStr.split(" ")
							self.ry = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,8,self.ry])
						elif 'BY: ' in dataStr :
							tmp = dataStr.split(" ")
							self.by = int(tmp[1])
							if self.isActif :
								self.pipeR.put([1,9,self.by])

					#print("Youpieeeeeeeeeee")
					else : # init ou memoire
						test = str(data[0].decode())
						strSplit = test.split('\n')
						#print(strSplit)
						for i in strSplit :
							if 'Red:' in i:		
								t = i.split(" ")
								self.red = int(t[1])
								if self.isActif :
									self.pipeR.put([1,0,self.red])
								print("RED ",self.red)
							elif 'Green: ' in i :
								t = i.split(" ")
								self.green = int(t[1])
								if self.isActif :
									self.pipeR.put([1,1,self.green])
							elif 'Blue: ' in i :
								t = i.split(" ")
								self.blue = int(t[1])
								if self.isActif :
									self.pipeR.put([1,2,self.blue])
							elif 'Black: ' in i :
								t = i.split(" ")
								self.black = int(t[1])
								if self.isActif :
									self.pipeR.put([1,3,self.black])
							elif 'Gain: ' in i :
								t = i.split(" ")
								self.gain = int(t[1])
								if self.isActif :
									self.pipeR.put([1,4,self.gain])
							elif 'Sharp: ' in i :
								t = i.split(" ")
								self.sharp = int(t[1])
								if self.isActif :
									self.pipeR.put([1,5,self.sharp])
							elif 'Hue: ' in i :
								t = i.split(" ")
								self.hue = int(t[1])
								if self.isActif :
									self.pipeR.put([1,6,self.hue])
							elif 'Saturation: ' in i :
								t = i.split(" ")
								self.sat = int(t[1])
								if self.isActif :
									self.pipeR.put([1,7,self.sat])
							elif 'RY: ' in i :
								t = i.split(" ")
								self.ry = int(t[1])
								if self.isActif :
									self.pipeR.put([1,8,self.ry])
							elif 'BY: ' in i :
								t = i.split(" ")
								self.by = int(t[1])
								if self.isActif :
									self.pipeR.put([1,9,self.by])
				#	print ("TESSSSSSSSSSSSSSSSSSSSSSSSSSSSST   ")
				except :
					print("Oups")

