#!/usr/bin/env python
#coding : ascii
from PyQt5 import QtWidgets
from ui_rcp import Ui_MainWindow  # importing our generated file
from  rcp_uiClass import mywindow
import time
import socket
import serial
import os
#import threading
import multiprocessing
from multiprocessing import Queue
from threading import Thread, RLock, Lock
from PyQt5.QtCore import QObject, pyqtSignal

class serialClass():
	def __init__(self,port,baud,pipe):
		self.baud = baud
		self.port=port
		self.pipe= pipe
		self.timer = 0
		self.serialP =  serial.Serial(self.port)
		self.serialP.timeout = 0
		self.serialP.baudrate = 115200

	def openPort(self):
		self.serialP.close()
		if self.serialP.is_open:
			print ('Teensy Serial at ',self.serialP.name,' is open')
		else :
			print ('Teensy port is close, try to open')
			self.serialP.open()
			if self.serialP.is_open:
				print ('Teensy Serial at  ',self.serialP.name,' is open')
				time.sleep(1)
			else :
				print ('error ,Teensy serial Close')


	def run(self):
		timeout = 0
		id =""
		while 1:
			#print("Pass")
		#	if time.time()-self.timer > 0.05 :
		#		id =""

				time.sleep(0.05)
				self.serialP.write('1'.encode('ascii'))
				timeout = time.time()
				while time.time() - timeout < 0.05 : 
					id = id + self.serialP.read().decode("ascii")
					
					#if not id == "" :
					#	print("Read is : ",id)
				if id [0:3] == "125" :
					id = id.split(" ")
					#print(id)
					if not id[1]== '0' :
						self.pipe.put([0,int(id[1])])
					if not id[2]== '0' :
						self.pipe.put([1,int(id[2])])
				id = ""
				
		#		self.timer= time.time()
				