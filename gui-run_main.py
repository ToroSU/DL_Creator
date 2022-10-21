import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QDockWidget, QListWidget
from PyQt5.QtGui import *
from Ui_DLC_GUI import Ui_Form

class mywindow(QtWidgets.QMainWindow, Ui_Form):
    #__init__:解構函式，也就是類被建立後就會預先載入的專案。
    # 馬上執行，這個方法可以用來對你的物件做一些你希望的初始化。
    def __init__(self):
        #這裡需要過載一下mywindow，同時也包含了QtWidgets.QMainWindow的預載入項。
        super(mywindow, self).__init__()
        self.setupUi(self)
 
 
if __name__ == '__main__': #如果整個程式是主程式
    # QApplication相當於main函式，也就是整個程式（很多檔案）的主入口函式。
    # 對於GUI程式必須至少有一個這樣的例項來讓程式執行。
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) # for high dpi scaling auto resize 
    app = QtWidgets.QApplication(sys.argv)
    #生成 mywindow 類的例項。
    window = mywindow()
    #有了例項，就得讓它顯示，show()是QWidget的方法，用於顯示視窗。
    window.show()
    # 呼叫sys庫的exit退出方法，條件是app.exec_()，也就是整個視窗關閉。
    # 有時候退出程式後，sys.exit(app.exec_())會報錯，改用app.exec_()就沒事
    # https://stackoverflow.com/questions/25719524/difference-between-sys-exitapp-exec-and-app-exec
    sys.exit(app.exec_())