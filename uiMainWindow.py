# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1428, 1114)
        MainWindow.setStyleSheet("background-color: rgb(70, 70, 70);\n"
"font: 11pt \"Sans Serif\";\n"
"color: rgb(209, 209, 209);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_video = QtWidgets.QWidget(self.centralwidget)
        self.widget_video.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_video.setMaximumSize(QtCore.QSize(10000, 4000))
        self.widget_video.setStyleSheet("background-color: rgb(52, 52, 52);")
        self.widget_video.setObjectName("widget_video")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_video)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_video = QtWidgets.QLabel(self.widget_video)
        self.lbl_video.setMinimumSize(QtCore.QSize(800, 450))
        self.lbl_video.setMaximumSize(QtCore.QSize(800, 450))
        self.lbl_video.setStyleSheet("background-color: rgb(6, 6, 6);")
        self.lbl_video.setText("")
        self.lbl_video.setObjectName("lbl_video")
        self.verticalLayout_2.addWidget(self.lbl_video)
        self.sld_video = QtWidgets.QSlider(self.widget_video)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sld_video.sizePolicy().hasHeightForWidth())
        self.sld_video.setSizePolicy(sizePolicy)
        self.sld_video.setOrientation(QtCore.Qt.Horizontal)
        self.sld_video.setObjectName("sld_video")
        self.verticalLayout_2.addWidget(self.sld_video)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_play_pause = QtWidgets.QPushButton(self.widget_video)
        self.btn_play_pause.setObjectName("btn_play_pause")
        self.horizontalLayout_3.addWidget(self.btn_play_pause)
        self.btn_stop = QtWidgets.QPushButton(self.widget_video)
        self.btn_stop.setObjectName("btn_stop")
        self.horizontalLayout_3.addWidget(self.btn_stop)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_video)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.widget_video)
        self.widget_status = QtWidgets.QWidget(self.centralwidget)
        self.widget_status.setStyleSheet("background-color: rgb(52, 52, 52);")
        self.widget_status.setObjectName("widget_status")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_status)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lay_delta_t = QtWidgets.QVBoxLayout()
        self.lay_delta_t.setObjectName("lay_delta_t")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lay_delta_t.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.lay_delta_t)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lbl_fps = QtWidgets.QLabel(self.widget_status)
        self.lbl_fps.setObjectName("lbl_fps")
        self.verticalLayout_4.addWidget(self.lbl_fps)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addWidget(self.widget_status)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.widget_multi = QtWidgets.QWidget(self.centralwidget)
        self.widget_multi.setMinimumSize(QtCore.QSize(300, 0))
        self.widget_multi.setStyleSheet("background-color: rgb(52, 52, 52);")
        self.widget_multi.setObjectName("widget_multi")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_multi)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.widget_multi)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(120, 120, 57, 15))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(100, 320, 80, 23))
        self.pushButton.setObjectName("pushButton")
        self.btn_add_detector = QtWidgets.QPushButton(self.tab)
        self.btn_add_detector.setGeometry(QtCore.QRect(50, 40, 181, 23))
        self.btn_add_detector.setObjectName("btn_add_detector")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout.addWidget(self.widget_multi)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1428, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_play_pause.setText(_translate("MainWindow", "Play"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_3.setText(_translate("MainWindow", "Open File"))
        self.lbl_fps.setText(_translate("MainWindow", "FPS: 0"))
        self.label.setText(_translate("MainWindow", "Test"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.btn_add_detector.setText(_translate("MainWindow", "Add Detector"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())