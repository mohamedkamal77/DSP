# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.map = QtWidgets.QWidget()
        self.map.setObjectName("map")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.map)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.map_layout = QtWidgets.QVBoxLayout()
        self.map_layout.setObjectName("map_layout")
        self.verticalLayout.addLayout(self.map_layout)
        self.map_control_layout = QtWidgets.QHBoxLayout()
        self.map_control_layout.setObjectName("map_control_layout")
        self.stop_2 = QtWidgets.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stop_2.setFont(font)
        self.stop_2.setFlat(True)
        self.stop_2.setObjectName("stop_2")
        self.map_control_layout.addWidget(self.stop_2)
        self.restart_2 = QtWidgets.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.restart_2.setFont(font)
        self.restart_2.setFlat(True)
        self.restart_2.setObjectName("restart_2")
        self.map_control_layout.addWidget(self.restart_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.map_control_layout.addItem(spacerItem)
        self.save_video_2 = QtWidgets.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_video_2.setFont(font)
        self.save_video_2.setFlat(True)
        self.save_video_2.setObjectName("save_video_2")
        self.map_control_layout.addWidget(self.save_video_2)
        self.hide_country = QtWidgets.QPushButton(self.map)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hide_country.setFont(font)
        self.hide_country.setFlat(True)
        self.hide_country.setObjectName("hide_country")
        self.map_control_layout.addWidget(self.hide_country)
        self.verticalLayout.addLayout(self.map_control_layout)
        self.videoprogress_2 = QtWidgets.QProgressBar(self.map)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoprogress_2.sizePolicy().hasHeightForWidth())
        self.videoprogress_2.setSizePolicy(sizePolicy)
        self.videoprogress_2.setProperty("value", 0)
        self.videoprogress_2.setObjectName("videoprogress_2")
        self.videoprogress_2.hide()
        self.verticalLayout.addWidget(self.videoprogress_2)
        self.verticalLayout.setStretch(0, 8)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.frame = QtWidgets.QFrame()
        self.on_click_layout = QtWidgets.QVBoxLayout()
        self.on_click_layout.setObjectName("on_click_layout")
        self.frame.setLayout(self.on_click_layout)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame.hide()
        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.map, "")
        self.buble = QtWidgets.QWidget()
        self.buble.setObjectName("buble")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.buble)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.buble1 = QtWidgets.QVBoxLayout()
        self.buble1.setObjectName("buble1")
        self.buble_layout = QtWidgets.QVBoxLayout()
        self.buble_layout.setObjectName("buble_layout")
        self.buble1.addLayout(self.buble_layout)
        self.buble_control_layout = QtWidgets.QHBoxLayout()
        self.buble_control_layout.setObjectName("buble_control_layout")
        self.stop_1 = QtWidgets.QPushButton(self.buble)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stop_1.setFont(font)
        self.stop_1.setFlat(True)
        self.stop_1.setObjectName("stop_1")
        self.buble_control_layout.addWidget(self.stop_1)
        self.restart_1 = QtWidgets.QPushButton(self.buble)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.restart_1.setFont(font)
        self.restart_1.setFlat(True)
        self.restart_1.setObjectName("restart_1")
        self.buble_control_layout.addWidget(self.restart_1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buble_control_layout.addItem(spacerItem1)
        self.save_video_1 = QtWidgets.QPushButton(self.buble)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_video_1.setFont(font)
        self.save_video_1.setFlat(True)
        self.save_video_1.setObjectName("save_video_1")
        self.buble_control_layout.addWidget(self.save_video_1)
        self.buble1.addLayout(self.buble_control_layout)
        self.videoprogress_1 = QtWidgets.QProgressBar(self.buble)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoprogress_1.sizePolicy().hasHeightForWidth())
        self.videoprogress_1.setSizePolicy(sizePolicy)
        self.videoprogress_1.setProperty("value", 0)
        self.videoprogress_1.setObjectName("videoprogress_1")
        self.videoprogress_1.hide()
        self.buble1.addWidget(self.videoprogress_1)
        self.buble1.setStretch(0, 8)
        self.buble1.setStretch(1, 1)
        self.buble1.setStretch(2, 1)
        self.verticalLayout_3.addLayout(self.buble1)
        self.tabWidget.addTab(self.buble, "")
        self.bar = QtWidgets.QWidget()
        self.bar.setObjectName("bar")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.bar)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.bar1 = QtWidgets.QVBoxLayout()
        self.bar1.setObjectName("bar1")
        self.bar_layout = QtWidgets.QVBoxLayout()
        self.bar_layout.setObjectName("bar_layout")
        self.bar1.addLayout(self.bar_layout)
        self.bar_control_layout = QtWidgets.QHBoxLayout()
        self.bar_control_layout.setObjectName("bar_control_layout")
        self.stop_3 = QtWidgets.QPushButton(self.bar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stop_3.setFont(font)
        self.stop_3.setFlat(True)
        self.stop_3.setObjectName("stop_3")
        self.bar_control_layout.addWidget(self.stop_3)
        self.restart_3 = QtWidgets.QPushButton(self.bar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.restart_3.setFont(font)
        self.restart_3.setFlat(True)
        self.restart_3.setObjectName("restart_3")
        self.bar_control_layout.addWidget(self.restart_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bar_control_layout.addItem(spacerItem2)
        self.save_video_3 = QtWidgets.QPushButton(self.bar)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_video_3.setFont(font)
        self.save_video_3.setFlat(True)
        self.save_video_3.setObjectName("save_video_3")
        self.bar_control_layout.addWidget(self.save_video_3)
        self.bar1.addLayout(self.bar_control_layout)
        self.videoprogress_3 = QtWidgets.QProgressBar(self.bar)
        self.videoprogress_3.setProperty("value", 0)
        self.videoprogress_3.setObjectName("videoprogress_3")
        self.bar1.addWidget(self.videoprogress_3)
        self.videoprogress_3.hide()
        self.bar1.setStretch(0, 8)
        self.bar1.setStretch(1, 1)
        self.bar1.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.bar1)
        self.tabWidget.addTab(self.bar, "")
        self.italy = QtWidgets.QWidget()
        self.italy.setObjectName("italy")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.italy)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.T_layout = QtWidgets.QHBoxLayout()
        self.T_layout.setObjectName("T_layout")
        self.verticalLayout_5.addLayout(self.T_layout)
        self.tabWidget.addTab(self.italy, "")
        self.verticalLayout_6.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 21))
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
        self.stop_2.setText(_translate("MainWindow", "Start"))
        self.restart_2.setText(_translate("MainWindow", "Restart"))
        self.save_video_2.setText(_translate("MainWindow", "Save Video"))
        self.hide_country.setText(_translate("MainWindow", "Hide Country"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.map), _translate("MainWindow", "World Map"))
        self.stop_1.setText(_translate("MainWindow", "Start"))
        self.restart_1.setText(_translate("MainWindow", "Restart"))
        self.save_video_1.setText(_translate("MainWindow", "Save Video"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.buble), _translate("MainWindow", "Buble Graph"))
        self.stop_3.setText(_translate("MainWindow", "Start"))
        self.restart_3.setText(_translate("MainWindow", "Restart"))
        self.save_video_3.setText(_translate("MainWindow", "Save Video"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bar), _translate("MainWindow", "Hbar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.italy), _translate("MainWindow", "Temprature Effect"))
        self.stop_li=[self.stop_2,self.stop_1,self.stop_3]
        self.save_li=[self.save_video_2,self.save_video_1,self.save_video_3]
        self.prpgress_li=[self.videoprogress_2,self.videoprogress_1,self.videoprogress_3]
