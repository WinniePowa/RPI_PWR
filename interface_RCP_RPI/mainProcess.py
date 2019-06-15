#!/usr/bin/env python
#coding : ascii
from PyQt5 import QtWidgets
from ui_rcp import Ui_MainWindow  # importing our generated file
from  rcp_uiClass import mywindow
import time
import socket
import os
#import threading
import multiprocessing
from multiprocessing import Queue
from threading import Thread, RLock, Lock
from teranexClass import teranex
from ip_unit import Ip_Unit
from PyQt5.QtCore import QObject, pyqtSignal
from serialClass import serialClass
	

	

def readInitFile(array) :
	file = open("ipInfo.txt",'r')
	file_contenu = file.read()
	file_contenu = file_contenu.split("/")
	array[0].addIpAddr(file_contenu[0])
	array[1].addIpAddr(file_contenu[1])
	array[2].addIpAddr(file_contenu[2])
	


def startMainProcess(pipeSendIhm,fromIhm,trig):
	ipClassArray = [Ip_Unit(),Ip_Unit(),Ip_Unit(),Ip_Unit()]
	readInitFile(ipClassArray) 
	activeItem = -1
	activeCam = 0

	pipeEArray= [Queue(),Queue(),Queue(),Queue()]
	pipeRTera = Queue()
	pipeFromEncoder = Queue()


	teranexArray = [teranex(0,pipeEArray[0],pipeRTera),teranex(1,pipeEArray[1],pipeRTera),teranex(2,pipeEArray[2],pipeRTera),teranex(3,pipeEArray[3],pipeRTera)] 
	
	processTera1 = multiprocessing.Process(target=teranexArray[0].run,args=())
	processTera1.start()
	processTera2 = multiprocessing.Process(target=teranexArray[1].run,args=())
	processTera2.start()
	processTera3 = multiprocessing.Process(target=teranexArray[2].run,args=())
	processTera3.start()
	processTera4 = multiprocessing.Process(target=teranexArray[3].run,args=())
	processTera4.start()


	serialObject = serialClass("/dev/ttyACM0",115200,pipeFromEncoder)
	serialObject.openPort()

	processSerial = multiprocessing.Process(target=serialObject.run,args=())
	processSerial.start()
	# Send Ip address to IHM
	pipeSendIhm.put([0,ipClassArray])
	#teranexArray.connection("192.168.0.10",9800)
	while 1 :
 
		if not fromIhm.empty() : # Pipe Ihm vers process
			data = fromIhm.get()
			if data[0] == 0 : #Le boutton Set Parameters a ete clicker, load nouvelle config IP
				print("From IHM ",data)
				teranexArray[0].closeConnection()
				teranexArray[1].closeConnection()
				if data[8] :
					print("Connection to : ",data[2])
					pipeEArray[0].put([-1,1])
					pipeEArray[0].put([2,data[2]])
					#teranexArray[0].connection(data[2],9800)
				if data[9] :
					print("Connection to : ",data[3])
					pipeEArray[1].put([2,data[3]])
				if data[10] :
					print("Connection to : ",data[4])
					pipeEArray[2].put([2,data[4]])
				if data[11] :
					print("Connection to : ",data[5])
					pipeEArray[3].put([2,data[5]])
					##teranexArray[1].connection(data[3],9800)
				#if data[6] :
			elif data[0] == 1 : #on  clicker sur uen des case du rcp  ou timer RAZ
				print ("case cocher is :",data[1]) 
				activeItem = data[1]
			elif data[0] == 2 : # active Camera changed
				for i in range(0,4) :
					if i == data[1] :
						activeCam = i
						print("New actif is : ",i)
						pipeEArray[i].put([-1,1])
					else :
						pipeEArray[i].put([-1,0])
		
		if not pipeFromEncoder.empty() :
			data = pipeFromEncoder.get()
			if data[0] == 0 : #Univ encoder
				print("Univ encoder : ",data[1]," Active Cam is ",activeCam)
				pipeEArray[activeCam].put([1,activeItem,data[1]])
				#teranexArray.send(activeItem,data[1])
			else :
				print("Iris encoder : ",data[1])

		if not pipeRTera.empty() : # Pipe  : serveur Ip vers IHM
			data = pipeRTera.get()
			#print (data)
			if data[0] == 1 : # set data
				pipeSendIhm.put([data[0],data[1],data[2]])
				#print("Youpie 2 ")
			elif data[0] == 2 : # on envoie otut les para d'un coup, changement de cam active
				pipeSendIhm.put([data[0],data[1]])
				print("Youpie")
			#	print("test")
			#	applicationIHM.MAJIHM(data[1],data[2])			

