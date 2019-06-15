from PyQt5 import QtWidgets
from ui_rcp import Ui_MainWindow  # importing our generated file
from  rcp_uiClass import mywindow
import asyncio
import threading
from ipClass import tcpClient
from multiprocessing import Queue
import sys
import multiprocessing
import mainProcess
from PyQt5.QtCore import QObject, pyqtSignal




pipeProcessToIhm = Queue()
pipeIhmToProcess = Queue()
app = QtWidgets.QApplication([])
application = mywindow(pipeProcessToIhm,pipeIhmToProcess)

process = multiprocessing.Process(target=mainProcess.startMainProcess,args=(pipeProcessToIhm,pipeIhmToProcess,application.trigger,))


process.start()
#tcp.tryConnection("192.168.0.30",7070)


application.show()
sys.exit(app.exec())


