
#!/usr/bin/python
import os,sys,time
from PyQt5 import QtWidgets, QtCore
from ui_rcp import Ui_MainWindow  # importing our generated file
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class Ip_Unit():
	def __init__(self):
		self.unit = 0
		self.R1 =""
		self.R2 =""
		self.M1=""
		self.M2=""
		self.M3=""
		self.P1=""
		self.P2=""
	def addIpAddr(self,str) :
		str = str.split('\n')
		self.unit = str[0]
		self.R1 = str[1][3:]
		self.R2 = str[2][3:]
		self.M1 = str[3][3:]
		self.M2 = str[4][3:]
		self.M3 = str[5][3:]
		self.P1 = str[6][3:]
		self.P2 = str[7][3:]