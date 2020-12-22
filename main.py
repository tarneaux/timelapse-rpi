# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'g.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

sleepTime = 1
savePath = "/media/pi/a13dcbf9-4836-41f4-bdcb-cfdc29c9e0df/"
stopper = 1

from time import sleep, time
from datetime import datetime
from os import system, chdir
from PyQt5 import QtCore, QtGui, QtWidgets
import threading

def makeTimeLapse():
    chdir(savePath)
    system("ls *.jpg > stills.txt")
    system("sudo mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=4/3:vbitrate=8000000 -vf scale=640:480 -o tlcam.avi -mf type=jpeg:fps=24 mf://@stills.txt")



class Ui_MainWindow(object):
    def timelapse(self, maxTime):
        global stopper, savePath, sleepTime
        try:
            ui = self
            ui.progressBar.setMaximum(maxTime)
            timeStart = time()
            while time() - timeStart < maxTime:
                t = time()
                ui.progressBar.setValue(t - timeStart)
                imageLocation = savePath + "img" + str(int(t)) + ".jpg"
                x = system("sudo raspistill -n -w 640 -h 480 -t " + str(sleepTime * 1000) + " -o " + imageLocation)
                if x != 0 or stopper == 1:
                    break
            ui.progressBar.setValue(maxTime)
            if stopper == 1:
                stopper = 2
                reply = system ("python3 dialog.py")
                print("reply is:", reply)
                if reply == 256:
                    self.pushButton.setText("Making the timelapse video...")
                    makeTimeLapse()
                self.pushButton.setText("Start timelapse")
                stopper = 1

            else:
                self.pushButton.setText("Making the timelapse video...")

        except KeyboardInterrupt:
            print("Ctrl+C pressed, exiting.")
            answerMakeTimeLapse = input("make the timelapse file? (Y/n)")
            if (answerMakeTimeLapse.upper() == "Y" or answerMakeTimeLapse == ""):
                print("making the timelapse")
            else:
                print("OK, exiting.")

    def onButtonPress(self):
        global savePath, sleepTime
        savePath = self.lineEdit.text()
        if savePath == "":
            savePath = "/media/pi/a13dcbf9-4836-41f4-bdcb-cfdc29c9e0df/"
        print(self.checkBox.checkState())
        if self.checkBox.checkState() == 2:
            print(self.timeEdit.time().toPyTime().strftime("%H%M"))
            while datetime.now().strftime("%H%M") != self.timeEdit.time().toPyTime().strftime("%H%M"):
                sleep(1)
        sleepTime = 60 / self.spinBox.value()
        self.timelapse(self.spinBox_2.value())

    def func(self):
        global stopper
        if stopper == 1:
            stopper = 0
            x = threading.Thread(target=self.onButtonPress)
            x.start()
            self.pushButton.setText("Stop timelapse")
        elif stopper == 0:
            stopper = 1
            self.pushButton.setText("Start timelapse")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(356, 330)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 351, 265))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(60)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinBox_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setRange(1, 2592000)
        self.spinBox_2.setValue(3600)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.timeEdit = QtWidgets.QTimeEdit(self.verticalLayoutWidget)
        self.timeEdit.setCalendarPopup(True)
        self.timeEdit.setObjectName("timeEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.timeEdit)
        self.checkBox = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.checkBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.func)
        self.verticalLayout.addWidget(self.pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 356, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Timelapse Shotter"))
        self.label_2.setText(_translate("MainWindow", " img/min"))
        self.label.setText(_translate("MainWindow", " max time"))
        self.label_3.setText(_translate("MainWindow", " save path"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "/home/pi/example"))
        self.checkBox.setText(_translate("MainWindow", "Start at"))
        self.pushButton.setText(_translate("MainWindow", "Start timelapse"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
