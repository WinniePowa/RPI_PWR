#!/usr/bin/python
import os,sys,time
from PyQt5 import QtWidgets, QtCore
from ui_rcp import Ui_MainWindow  # importing our generated file
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ip_unit import Ip_Unit

class mywindow(QtWidgets.QMainWindow):
	trigger = pyqtSignal()
	def __init__(self,pipe,pipeToProcess):
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.minX = 30
		self.minY = 145
		self.xLargeur = 240
		self.yLargeur =  150
		self.activeItem = -1
		self.timerRAZ = QTimer()
		self.mapper = QSignalMapper(self)
		self.pipe = pipe
		self.pipeToProcess = pipeToProcess
		self.ipClassArray = [Ip_Unit(),Ip_Unit(),Ip_Unit(),Ip_Unit()]
		self.readInitFile(self.ipClassArray)
		self.ui.main_Combo.addItems(["Unit 1","Unit 2","Unit 3","Unit 4"])
		self.setComboBox(self.ipClassArray[0])
		self.ui.main_Combo.currentIndexChanged.connect(self.mainComboChange)
		self.ui.set_button.clicked.connect(self.setParaHasBeenClicked)
		self.mapper.setMapping(self.ui.Camera1,0)
		self.ui.Camera1.clicked.connect(self.mapper.map)
		self.mapper.setMapping(self.ui.Camera2,1)
		self.ui.Camera2.clicked.connect(self.mapper.map)
		self.mapper.setMapping(self.ui.Camera3,2)
		self.ui.Camera3.clicked.connect(self.mapper.map)
		self.mapper.setMapping(self.ui.Camera4,3)
		self.ui.Camera4.clicked.connect(self.mapper.map)
		self.mapper.setMapping(self.ui.Camera5,4)
		self.ui.Camera5.clicked.connect(self.mapper.map)

		self.mapper.mapped[int].connect(self.activeCamChanged)
		self.thread = Worker(self.pipe)
		self.thread.test.connect(self.MAJIHM)
		#self.connect(self.thread, SIGNAL("test()"), self.MAJIHM)
		self.thread.start()
		self.timerRAZ.setSingleShot(1)
		self.timerRAZ.setInterval(5000)
		self.timerRAZ.timeout.connect(self.timeOutRAZ)



	@pyqtSlot(int)
	def activeCamChanged(self, name):
		#print("Active Cam changed ! ",name)
		self.ui.displayCamNumber.display(name)
		self.pipeToProcess.put([2,name])

	def timeOutRAZ(self):
		self.activeItem = -1
		self.pipeToProcess.put([1,self.activeItem])
		self.resetAllCase()

	def setParaHasBeenClicked(self):
		print("Set has been Pressed")
		#[ 0 ,Unit_Index ,R1_Ip , R2_IP , M1_IP , M2_IP , R1_C , R2_C , M1_C , M2_C ]
		self.pipeToProcess.put([0,self.ui.main_Combo.currentIndex(),
			self.ui.R1_combo.currentText(),
			self.ui.R2_combo.currentText(),
			self.ui.M1_combo.currentText(),
			self.ui.M2_combo.currentText(),
			self.ui.PC1_combo.currentText(),
			self.ui.PC2_combo.currentText(),
			self.ui.R1_box.isChecked(),
			self.ui.R2_box.isChecked(),
			self.ui.M1_box.isChecked(),
			self.ui.M2_box.isChecked(),])

	def mainComboChange(self,index):
		self.setComboBox(self.ipClassArray[index])

	def setComboBox(self,ipCLass):
		self.ui.R1_combo.clear()
		self.ui.R2_combo.clear()
		self.ui.M1_combo.clear()
		self.ui.M2_combo.clear()
		self.ui.PC2_combo.clear()
		self.ui.PC1_combo.clear()

		self.ui.R1_combo.addItems([ipCLass.R1])
		self.ui.R2_combo.addItems([ipCLass.R2])
		self.ui.PC1_combo.addItems([ipCLass.P1])
		self.ui.PC2_combo.addItems([ipCLass.P2])
		self.ui.M1_combo.addItems([ipCLass.M1,ipCLass.M2,ipCLass.M3])
		self.ui.M2_combo.addItems([ipCLass.M1,ipCLass.M2,ipCLass.M3])
		self.ui.M2_combo.setCurrentIndex(1)

	def readInitFile(self,array) :
		file = open("ipInfo.txt",'r')
		file_contenu = file.read()
		file_contenu = file_contenu.split("/")
		array[0].addIpAddr(file_contenu[0])
		array[1].addIpAddr(file_contenu[1])
		array[2].addIpAddr(file_contenu[2])

	def resetAllCase(self) :
		self.ui.red_B.setStyleSheet("QGroupBox{background-color:red;border: 8px solid red;}QLCDNumber{background-color : red;}")
		self.ui.green_B.setStyleSheet("QGroupBox{background-color:green;border: 8px solid green;}QLCDNumber{background-color : green;}")
		self.ui.blue_B.setStyleSheet("QGroupBox{background-color:blue;border: 8px solid blue;}QLCDNumber{background-color : blue;}")
		self.ui.black_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.gamma_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.sharp_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.sat_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")	  	
		self.ui.gain_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.hue_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.ry_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
		self.ui.by_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")

	def mouseReleaseEvent(self, QMouseEvent):
		#print('(', QMouseEvent.x(), ', ', QMouseEvent.y(), ')')
		#print('(', int((QMouseEvent.x()- self.minX)/ self.xLargeur), ', ', int((QMouseEvent.y()-self.minY) / self.yLargeur), ')')
		cellule = 3*(int((QMouseEvent.y()-self.minY) / self.yLargeur))  + int((QMouseEvent.x()- self.minX) / self.xLargeur)
		if self.ui.colorTab.currentIndex() == 0 :
			print (cellule)
			self.activeItem = cellule
			self.timerRAZ.start()
			self.pipeToProcess.put([1,self.activeItem])
			if (cellule == 0):
				self.ui.red_B.setStyleSheet("QGroupBox{background-color:red;border: 8px solid green;}QLCDNumber{background-color : red;}")
			else :
	  	 		self.ui.red_B.setStyleSheet("QGroupBox{background-color:red;border: 8px solid red;}QLCDNumber{background-color : red;}")
			if (cellule == 1):
				self.ui.green_B.setStyleSheet("QGroupBox{background-color:green;border: 8px solid blue;}QLCDNumber{background-color : green;}")
			else :
	  	 		self.ui.green_B.setStyleSheet("QGroupBox{background-color:green;border: 8px solid green;}QLCDNumber{background-color : green;}")
			if (cellule == 2):
				self.ui.blue_B.setStyleSheet("QGroupBox{background-color:blue;border: 8px solid green;}QLCDNumber{background-color : blue;}")
			else :
	  	 		self.ui.blue_B.setStyleSheet("QGroupBox{background-color:blue;border: 8px solid blue;}QLCDNumber{background-color : blue;}")
			if (cellule == 3):
				self.ui.black_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.black_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 4):
				self.ui.gamma_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.gamma_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 5):
				self.ui.sharp_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.sharp_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 6):
				self.ui.sat_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.sat_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")	  	 			  	 		
			if (cellule == 8):
				self.ui.gain_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.gain_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 9):
				self.ui.hue_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.hue_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 10):
				self.ui.ry_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.ry_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
			if (cellule == 11):
				self.ui.by_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid red;}QLCDNumber{background-color : #2C2C2C;}")
			else :
	  	 		self.ui.by_B.setStyleSheet("QGroupBox{background-color:#2C2C2C;border: 8px solid #2C2C2C;}QLCDNumber{background-color : #2C2C2C;}")
				  	 			  	 			  	 		
		elif self.ui.colorTab.currentIndex() == 1 :
			print ("Tab 2!")
		elif self.ui.colorTab.currentIndex() == 2 :
			print ("Ip setting Page !!")

	def red_B_Press(self):
		print ("youpie")
	def MAJIHM(self,item,value):
		("QGroupBox{background-color:red;border: 8px solid green;}QLCDNumber{background-color : red;}")
		if item == 0 :
			self.ui.red_lcd.display(value)
			self.ui.red_bar.setValue(value)
		elif item == 1 :
			self.ui.green_lcd.display(value)
			self.ui.green_bar.setValue(value)
		elif item == 2 :
			self.ui.blue_lcd.display(value)
			self.ui.blue_bar.setValue(value)
		elif item == 3 :
			self.ui.black_lcd.display(value)
			self.ui.black_bar.setValue(value)
		elif item == 4 :
			self.ui.gain_lcd.display(value)
			self.ui.gain_bar.setValue(value)
		elif item == 5 :
			self.ui.sharp_lcd.display(value)
			self.ui.sharp_bar.setValue(value)
		elif item == 6 :
			self.ui.hue_lcd.display(value)
			self.ui.hue_bar.setValue(value)
		elif item == 7 :
			self.ui.sat_lcd.display(value)
			self.ui.sat_bar.setValue(value)
		elif item == 8 :
			self.ui.ry_lcd.display(value)
			self.ui.ry_bar.setValue(value)
		elif item == 9 :
			self.ui.by_lcd.display(value)
			self.ui.by_bar.setValue(value)
		elif item == 10 :
			if value == False :
				self.ui.deco_label.setText("Disconnected")
				self.ui.deco_label.setStyleSheet("QLabel{color : red;}")
			else :
				self.ui.deco_label.setText("Connected")
				self.ui.deco_label.setStyleSheet("QLabel{color : green;}")



class Worker(QThread):
	test = pyqtSignal(int,int )
	def __init__(self, pipe,parent=None):
		QThread.__init__(self, parent)
		self.pipe = pipe

	def run(self):
		while 1 :
			#print("running")
			if not self.pipe.empty() :
				data = self.pipe.get()
				if  data[0] == 1: # MAJ 1 parametre
					self.test.emit(int(data[1]),int(data[2]))
				elif data[0] == 2 : # MAJ TOUS parametre
					for i in range(0,11):
						self.test.emit(i,int(data[1][i]))
					#self.test.emit(0,int(data[1][0]))
					#self.test.emit(1,int(data[1][0]))
					#self.test.emit(2,int(data[1][0]))
				#else :
				#	self.