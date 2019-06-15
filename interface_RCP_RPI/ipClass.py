#!/usr/bin/python3
import os,sys,time
import socket
from multiprocessing import Queue
import multiprocessing
from threading import Thread, RLock, Lock
import _thread


class tcpClient():
	def __init__(self,name,pipeE,pipeR):
		self.addr=""
		self.port = 0
		self.connected = False
		self.name = name
		self.pipeE = pipeE
		self.pipeR = pipeR
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#_thread.start_new_thread(self.handler, (self.socket,self.addr))

	def closeConnection(self):
		self.connected = False
		#time.sleep(0.5)
		try :
			self.socket.close()
			#print("YOupie")
			#self.socket.shutdown()
		#	self.socket.close()
		except :
			print("Error close connection")

	def tryConnection(self,address,port):
		self.addr = address
		self.port = port
		#time.sleep(1)

		try :
			print ("Connection...")
			self.socket.close()
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			_thread.start_new_thread(self.handler, (self.socket,self.addr))
			self.socket.connect((self.addr,self.port))
			self.connected = True
			print ("Connection OK !")
		except :
			print ("Erorr Socket connection")
			#print("Unexpected error:", sys.exc_info())
	def sendToSocket(self,status,stringToSend):
		if self.connected :
			rall = '\n'
			self.socket.send(status.encode())
			self.socket.send(stringToSend.encode())
			self.socket.send(rall.encode())
	def isConnected(self):
		return self.connected

	def handler(self,socket,addr):
		print ('Fonction handler start)')
		while 1:
			if self.connected == True :
				data = socket.recv(1024)
				self.pipeR.put([data])
				#print (data)
