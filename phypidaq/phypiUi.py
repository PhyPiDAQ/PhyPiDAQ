# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'phypi.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PhyPiWindow(object):
    def setupUi(self, PhyPiWindow):
        PhyPiWindow.setObjectName("PhyPiWindow")
        PhyPiWindow.resize(705, 601)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PhyPiWindow.sizePolicy().hasHeightForWidth())
        PhyPiWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(PhyPiWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.central_layout.setObjectName("central_layout")
        self.tab_Main = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_Main.setGeometry(QtCore.QRect(-1, 0, 711, 601))
        self.tab_Main.setStatusTip("")
        self.tab_Main.setObjectName("tab_Main")
        self.Tab_Control = QtWidgets.QWidget()
        self.Tab_Control.setWhatsThis("")
        self.Tab_Control.setObjectName("Tab_Control")
        self.tab_control_layout = QtWidgets.QVBoxLayout(self.Tab_Control)
        self.tab_control_layout.setObjectName("tab_control_layout")
        self.stop_button_layout = QtWidgets.QHBoxLayout()
        self.stop_button_layout.setObjectName("stop_button_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.stop_button_layout.addItem(spacerItem)
        self.pB_abort = QtWidgets.QPushButton(self.Tab_Control)
        self.pB_abort.setGeometry(QtCore.QRect(660, 0, 41, 41))
        self.pB_abort.setAccessibleDescription("")
        self.pB_abort.setText("")
        icon = QtGui.QIcon.fromTheme(":/icons/application-exit")
        self.pB_abort.setIcon(icon)
        self.pB_abort.setIconSize(QtCore.QSize(20, 20))
        self.pB_abort.setAutoDefault(False)
        self.pB_abort.setObjectName("pB_abort")
        self.stop_button_layout.addWidget(self.pB_abort)
        self.tab_control_layout.addLayout(self.stop_button_layout)
        self.logo_widget = QtWidgets.QWidget(self.Tab_Control)
        self.logo_widget.setObjectName("logo_widget")
        self.logo_widget_layout = QtWidgets.QHBoxLayout(self.logo_widget)
        self.logo_widget_layout.setObjectName("logo_widget_layout")
        self.label_Picture = QtWidgets.QLabel(self.logo_widget)
        self.label_Picture.setGeometry(QtCore.QRect(160, 250, 90, 70))
        self.label_Picture.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_Picture.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label_Picture.setText("")
        self.label_Picture.setPixmap(QtGui.QPixmap("images/PhiPiLogo.png"))
        self.label_Picture.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Picture.setObjectName("label_Picture")
        self.logo_widget_layout.addWidget(self.label_Picture)
        self.label_caption = QtWidgets.QLabel(self.logo_widget)
        self.label_caption.setGeometry(QtCore.QRect(230, 220, 391, 141))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_caption.setFont(font)
        self.label_caption.setObjectName("label_caption")
        self.logo_widget_layout.addWidget(self.label_caption)
        self.tab_control_layout.addWidget(self.logo_widget)
        self.label_2 = QtWidgets.QLabel(self.Tab_Control)
        self.label_2.setGeometry(QtCore.QRect(80, 50, 551, 171))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("images/PhyPiDAQdiagram.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.tab_control_layout.addWidget(self.label_2)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_DAQconfig = QtWidgets.QLabel(self.Tab_Control)
        self.label_DAQconfig.setGeometry(QtCore.QRect(60, 426, 91, 30))
        font = QtGui.QFont()
        font.setFamily("Latin Modern Sans")
        font.setPointSize(11)
        self.label_DAQconfig.setFont(font)
        self.label_DAQconfig.setTextFormat(QtCore.Qt.PlainText)
        self.label_DAQconfig.setObjectName("label_DAQconfig")
        self.hboxlayout.addWidget(self.label_DAQconfig)
        self.lE_DAQConfFile = QtWidgets.QLineEdit(self.Tab_Control)
        self.lE_DAQConfFile.setGeometry(QtCore.QRect(160, 430, 371, 32))
        self.lE_DAQConfFile.setText("")
        self.lE_DAQConfFile.setReadOnly(True)
        self.lE_DAQConfFile.setObjectName("lE_DAQConfFile")
        self.hboxlayout.addWidget(self.lE_DAQConfFile)
        self.pB_FileSelect = QtWidgets.QPushButton(self.Tab_Control)
        self.pB_FileSelect.setGeometry(QtCore.QRect(540, 430, 31, 34))
        self.pB_FileSelect.setText("")
        icon = QtGui.QIcon.fromTheme("folder-open")
        self.pB_FileSelect.setIcon(icon)
        self.pB_FileSelect.setObjectName("pB_FileSelect")
        self.hboxlayout.addWidget(self.pB_FileSelect)
        self.tab_control_layout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtWidgets.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label_WorkDir = QtWidgets.QLabel(self.Tab_Control)
        self.label_WorkDir.setGeometry(QtCore.QRect(76, 386, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Latin Modern Sans")
        font.setPointSize(11)
        self.label_WorkDir.setFont(font)
        self.label_WorkDir.setObjectName("label_WorkDir")
        self.hboxlayout1.addWidget(self.label_WorkDir)
        self.lE_WorkDir = QtWidgets.QLineEdit(self.Tab_Control)
        self.lE_WorkDir.setGeometry(QtCore.QRect(160, 380, 371, 32))
        self.lE_WorkDir.setReadOnly(True)
        self.lE_WorkDir.setObjectName("lE_WorkDir")
        self.hboxlayout1.addWidget(self.lE_WorkDir)
        self.pB_WDselect = QtWidgets.QPushButton(self.Tab_Control)
        self.pB_WDselect.setGeometry(QtCore.QRect(540, 380, 31, 34))
        self.pB_WDselect.setText("")
        icon = QtGui.QIcon.fromTheme("folder-open")
        self.pB_WDselect.setIcon(icon)
        self.pB_WDselect.setObjectName("pB_WDselect")
        self.hboxlayout1.addWidget(self.pB_WDselect)
        self.tab_control_layout.addLayout(self.hboxlayout1)
        self.hboxlayout2 = QtWidgets.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)
        self.pB_StartRun = QtWidgets.QPushButton(self.Tab_Control)
        self.pB_StartRun.setGeometry(QtCore.QRect(591, 524, 101, 40))
        icon = QtGui.QIcon.fromTheme("start-here")
        self.pB_StartRun.setIcon(icon)
        self.pB_StartRun.setIconSize(QtCore.QSize(24, 24))
        self.pB_StartRun.setObjectName("pB_StartRun")
        self.hboxlayout2.addWidget(self.pB_StartRun)
        self.tab_control_layout.addLayout(self.hboxlayout2)
        self.tab_Main.addTab(self.Tab_Control, "")
        self.Tab_Config = QtWidgets.QWidget()
        self.Tab_Config.setObjectName("Tab_Config")
        self.tab_config_layout = QtWidgets.QVBoxLayout(self.Tab_Config)
        self.tab_config_layout.setObjectName("tab_config_layout")
        self.rB_EditMode = QtWidgets.QRadioButton(self.Tab_Config)
        self.rB_EditMode.setGeometry(QtCore.QRect(580, 10, 111, 30))
        self.rB_EditMode.setObjectName("rB_EditMode")
        self.tab_config_layout.addWidget(self.rB_EditMode)
        self.tabConfig = QtWidgets.QTabWidget(self.Tab_Config)
        self.tabConfig.setEnabled(True)
        self.tabConfig.setGeometry(QtCore.QRect(10, 10, 821, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabConfig.sizePolicy().hasHeightForWidth())
        self.tabConfig.setSizePolicy(sizePolicy)
        self.tabConfig.setMinimumSize(QtCore.QSize(811, 0))
        self.tabConfig.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabConfig.setObjectName("tabConfig")
        self.tab_phypiConfig = QtWidgets.QWidget()
        self.tab_phypiConfig.setEnabled(True)
        self.tab_phypiConfig.setObjectName("tab_phypiConfig")
        self.tab_phypiConfig_layout = QtWidgets.QVBoxLayout(self.tab_phypiConfig)
        self.tab_phypiConfig_layout.setObjectName("tab_phypiConfig_layout")
        self.pTE_phypiConfig = QtWidgets.QPlainTextEdit(self.tab_phypiConfig)
        self.pTE_phypiConfig.setGeometry(QtCore.QRect(0, 10, 681, 431))
        self.pTE_phypiConfig.setReadOnly(True)
        self.pTE_phypiConfig.setObjectName("pTE_phypiConfig")
        self.tab_phypiConfig_layout.addWidget(self.pTE_phypiConfig)
        self.pB_reloadConfig = QtWidgets.QPushButton(self.tab_phypiConfig)
        self.pB_reloadConfig.setEnabled(False)
        self.pB_reloadConfig.setGeometry(QtCore.QRect(500, 440, 171, 21))
        icon = QtGui.QIcon.fromTheme("list-add")
        self.pB_reloadConfig.setIcon(icon)
        self.pB_reloadConfig.setCheckable(False)
        self.pB_reloadConfig.setChecked(False)
        self.pB_reloadConfig.setAutoDefault(False)
        self.pB_reloadConfig.setObjectName("pB_reloadConfig")
        self.tab_phypiConfig_layout.addWidget(self.pB_reloadConfig)
        self.tabConfig.addTab(self.tab_phypiConfig, "")
        self.tab_DeviceConfig0 = QtWidgets.QWidget()
        self.tab_DeviceConfig0.setObjectName("tab_DeviceConfig0")
        self.tab_DeviceConfig0_layout = QtWidgets.QVBoxLayout(self.tab_DeviceConfig0)
        self.tab_DeviceConfig0_layout.setObjectName("tab_DeviceConfig0_layout")
        self.pTE_DeviceConfig0 = QtWidgets.QPlainTextEdit(self.tab_DeviceConfig0)
        self.pTE_DeviceConfig0.setGeometry(QtCore.QRect(0, 10, 681, 411))
        self.pTE_DeviceConfig0.setReadOnly(True)
        self.pTE_DeviceConfig0.setObjectName("pTE_DeviceConfig0")
        self.tab_DeviceConfig0_layout.addWidget(self.pTE_DeviceConfig0)
        self.pB_DeviceSelect0 = QtWidgets.QPushButton(self.tab_DeviceConfig0)
        self.pB_DeviceSelect0.setGeometry(QtCore.QRect(490, 423, 181, 34))
        self.pB_DeviceSelect0.setObjectName("pB_DeviceSelect0")
        self.tab_DeviceConfig0_layout.addWidget(self.pB_DeviceSelect0)
        self.tabConfig.addTab(self.tab_DeviceConfig0, "")
        self.tab_DeviceConfig1 = QtWidgets.QWidget()
        self.tab_DeviceConfig1.setEnabled(False)
        self.tab_DeviceConfig1.setObjectName("tab_DeviceConfig1")
        self.tab_DeviceConfig1_layout = QtWidgets.QVBoxLayout(self.tab_DeviceConfig1)
        self.tab_DeviceConfig1_layout.setObjectName("tab_DeviceConfig1_layout")
        self.pTE_DeviceConfig1 = QtWidgets.QPlainTextEdit(self.tab_DeviceConfig1)
        self.pTE_DeviceConfig1.setGeometry(QtCore.QRect(0, 0, 681, 421))
        self.pTE_DeviceConfig1.setReadOnly(True)
        self.pTE_DeviceConfig1.setObjectName("pTE_DeviceConfig1")
        self.tab_DeviceConfig1_layout.addWidget(self.pTE_DeviceConfig1)
        self.pB_DeviceSelect1 = QtWidgets.QPushButton(self.tab_DeviceConfig1)
        self.pB_DeviceSelect1.setGeometry(QtCore.QRect(490, 423, 181, 34))
        self.pB_DeviceSelect1.setObjectName("pB_DeviceSelect1")
        self.tab_DeviceConfig1_layout.addWidget(self.pB_DeviceSelect1)
        self.tabConfig.addTab(self.tab_DeviceConfig1, "")
        self.tab_DeviceConfig2 = QtWidgets.QWidget()
        self.tab_DeviceConfig2.setEnabled(False)
        self.tab_DeviceConfig2.setObjectName("tab_DeviceConfig2")
        self.tab_DeviceConfig2_layout = QtWidgets.QVBoxLayout(self.tab_DeviceConfig2)
        self.tab_DeviceConfig2_layout.setObjectName("tab_DeviceConfig2_layout")
        self.pTE_DeviceConfig2 = QtWidgets.QPlainTextEdit(self.tab_DeviceConfig2)
        self.pTE_DeviceConfig2.setGeometry(QtCore.QRect(0, 0, 681, 421))
        self.pTE_DeviceConfig2.setReadOnly(True)
        self.pTE_DeviceConfig2.setObjectName("pTE_DeviceConfig2")
        self.tab_DeviceConfig2_layout.addWidget(self.pTE_DeviceConfig2)
        self.pB_DeviceSelect2 = QtWidgets.QPushButton(self.tab_DeviceConfig2)
        self.pB_DeviceSelect2.setGeometry(QtCore.QRect(490, 423, 181, 34))
        self.pB_DeviceSelect2.setObjectName("pB_DeviceSelect2")
        self.tab_DeviceConfig2_layout.addWidget(self.pB_DeviceSelect2)
        self.tabConfig.addTab(self.tab_DeviceConfig2, "")
        self.tab_config_layout.addWidget(self.tabConfig)
        self.tab_Main.addTab(self.Tab_Config, "")
        self.Tab_Help = QtWidgets.QWidget()
        self.Tab_Help.setObjectName("Tab_Help")
        self.tab_help_layout = QtWidgets.QVBoxLayout(self.Tab_Help)
        self.tab_help_layout.setObjectName("tab_help_layout")
        self.tab_help_buttons = QtWidgets.QWidget(self.Tab_Help)
        self.tab_help_buttons.setObjectName("tab_help_buttons")
        self.tab_help_buttons_layout = QtWidgets.QHBoxLayout(self.tab_help_buttons)
        self.tab_help_buttons_layout.setObjectName("tab_help_buttons_layout")
        self.pB_Help = QtWidgets.QPushButton(self.tab_help_buttons)
        self.pB_Help.setGeometry(QtCore.QRect(10, 0, 88, 31))
        icon = QtGui.QIcon.fromTheme(":/icons/flag-EN")
        self.pB_Help.setIcon(icon)
        self.pB_Help.setObjectName("pB_Help")
        self.tab_help_buttons_layout.addWidget(self.pB_Help)
        self.pB_Hilfe = QtWidgets.QPushButton(self.tab_help_buttons)
        self.pB_Hilfe.setGeometry(QtCore.QRect(110, 0, 88, 31))
        icon = QtGui.QIcon.fromTheme(":/icons/flag-DE")
        self.pB_Hilfe.setIcon(icon)
        self.pB_Hilfe.setObjectName("pB_Hilfe")
        self.tab_help_buttons_layout.addWidget(self.pB_Hilfe)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.tab_help_buttons_layout.addItem(spacerItem2)
        self.tab_help_layout.addWidget(self.tab_help_buttons)
        self.TE_Help = QtWidgets.QTextEdit(self.Tab_Help)
        self.TE_Help.setGeometry(QtCore.QRect(10, 30, 691, 481))
        self.TE_Help.setUndoRedoEnabled(False)
        self.TE_Help.setReadOnly(True)
        self.TE_Help.setPlaceholderText("")
        self.TE_Help.setObjectName("TE_Help")
        self.tab_help_layout.addWidget(self.TE_Help)
        self.tab_Main.addTab(self.Tab_Help, "")
        self.central_layout.addWidget(self.tab_Main)
        self.main_button_widget = QtWidgets.QWidget(self.centralwidget)
        self.main_button_widget.setObjectName("main_button_widget")
        self.main_button_layout = QtWidgets.QHBoxLayout(self.main_button_widget)
        self.main_button_layout.setObjectName("main_button_layout")
        self.label = QtWidgets.QLabel(self.main_button_widget)
        self.label.setGeometry(QtCore.QRect(30, 550, 60, 31))
        font = QtGui.QFont()
        font.setFamily("Latin Modern Sans")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.main_button_layout.addWidget(self.label)
        self.lE_RunTag = QtWidgets.QLineEdit(self.main_button_widget)
        self.lE_RunTag.setGeometry(QtCore.QRect(99, 552, 113, 30))
        self.lE_RunTag.setObjectName("lE_RunTag")
        self.main_button_layout.addWidget(self.lE_RunTag)
        self.pB_SaveDefault = QtWidgets.QPushButton(self.main_button_widget)
        self.pB_SaveDefault.setGeometry(QtCore.QRect(230, 550, 141, 34))
        self.pB_SaveDefault.setObjectName("pB_SaveDefault")
        self.main_button_layout.addWidget(self.pB_SaveDefault)
        self.central_layout.addWidget(self.main_button_widget)
        PhyPiWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PhyPiWindow)
        self.tab_Main.setCurrentIndex(0)
        self.tabConfig.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PhyPiWindow)

    def retranslateUi(self, PhyPiWindow):
        _translate = QtCore.QCoreApplication.translate
        PhyPiWindow.setWindowTitle(_translate("PhyPiWindow", "PhiPiDAQ"))
        self.tab_Main.setToolTip(_translate("PhyPiWindow", "Output / Configuration / Help"))
        self.Tab_Control.setToolTip(_translate("PhyPiWindow", "Control Panel"))
        self.pB_abort.setToolTip(_translate("PhyPiWindow", "Exit PhyPi Gui"))
        self.label_Picture.setToolTip(_translate("PhyPiWindow", "PhyPi Data Acquisition with Raspberry Pi"))
        self.label_caption.setText(
            _translate(
                "PhyPiWindow",
                "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">D</span><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">ata </span><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">A</span><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">c</span><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">q</span><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">uisition </span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">for </span><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">Phy</span><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">sics </span></p><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#00007f;\">with Raspberry </span><span style=\" font-size:16pt; font-weight:600; color:#0000ff;\">Pi</span><span style=\" font-size:16pt; font-weight:600; color:#00007f;\"/></p></body></html>",
            )
        )
        self.label_DAQconfig.setText(_translate("PhyPiWindow", "DAQ config:"))
        self.lE_DAQConfFile.setToolTip(_translate("PhyPiWindow", "DAQ configuration file (type .daq)"))
        self.pB_FileSelect.setToolTip(_translate("PhyPiWindow", "Selected daq configuration file"))
        self.label_WorkDir.setText(_translate("PhyPiWindow", "Work Dir:"))
        self.pB_WDselect.setToolTip(_translate("PhyPiWindow", "select working directory (where output is stored)"))
        self.pB_StartRun.setToolTip(_translate("PhyPiWindow", "Start Data Acquisition"))
        self.pB_StartRun.setText(_translate("PhyPiWindow", "Start Run"))
        self.tab_Main.setTabText(self.tab_Main.indexOf(self.Tab_Control), _translate("PhyPiWindow", "Control"))
        self.Tab_Config.setToolTip(_translate("PhyPiWindow", "Config Panel"))
        self.rB_EditMode.setText(_translate("PhyPiWindow", "Edit Mode"))
        self.tabConfig.setToolTip(_translate("PhyPiWindow", "Configuration Files"))
        self.tab_phypiConfig.setToolTip(_translate("PhyPiWindow", "PhyPi Configuration"))
        self.pTE_phypiConfig.setToolTip(_translate("PhyPiWindow", "Main PhyPi Configuration File"))
        self.pB_reloadConfig.setToolTip(
            _translate("PhyPiWindow", "reload device configuration files if names or paths changed")
        )
        self.pB_reloadConfig.setText(_translate("PhyPiWindow", "reload device config(s)"))
        self.tabConfig.setTabText(
            self.tabConfig.indexOf(self.tab_phypiConfig), _translate("PhyPiWindow", "PhyPi Config")
        )
        self.tab_DeviceConfig0.setToolTip(_translate("PhyPiWindow", "(1st) Device Configuration"))
        self.pTE_DeviceConfig0.setToolTip(_translate("PhyPiWindow", "Device Configuration"))
        self.pB_DeviceSelect0.setToolTip(_translate("PhyPiWindow", "load template device configuration"))
        self.pB_DeviceSelect0.setText(_translate("PhyPiWindow", "load Device Config"))
        self.tabConfig.setTabText(
            self.tabConfig.indexOf(self.tab_DeviceConfig0), _translate("PhyPiWindow", "Device Config")
        )
        self.tab_DeviceConfig1.setToolTip(_translate("PhyPiWindow", "2nd Device Configuration"))
        self.pB_DeviceSelect1.setText(_translate("PhyPiWindow", "load Device Config"))
        self.tabConfig.setTabText(
            self.tabConfig.indexOf(self.tab_DeviceConfig1), _translate("PhyPiWindow", "2nd Device")
        )
        self.pB_DeviceSelect2.setText(_translate("PhyPiWindow", "load Device Config"))
        self.tabConfig.setTabText(
            self.tabConfig.indexOf(self.tab_DeviceConfig2), _translate("PhyPiWindow", "3rd Device")
        )
        self.tab_Main.setTabText(self.tab_Main.indexOf(self.Tab_Config), _translate("PhyPiWindow", "Configuration"))
        self.Tab_Help.setToolTip(_translate("PhyPiWindow", "Info & Help"))
        self.pB_Help.setText(_translate("PhyPiWindow", "English"))
        self.pB_Hilfe.setText(_translate("PhyPiWindow", "Deutsch"))
        self.tab_Main.setTabText(self.tab_Main.indexOf(self.Tab_Help), _translate("PhyPiWindow", "Help / Hilfe"))
        self.label.setWhatsThis(_translate("PhyPiWindow", "common name"))
        self.label.setText(_translate("PhyPiWindow", "Name:"))
        self.lE_RunTag.setToolTip(_translate("PhyPiWindow", "Name for the run"))
        self.lE_RunTag.setText(_translate("PhyPiWindow", "phypi"))
        self.pB_SaveDefault.setToolTip(_translate("PhyPiWindow", "save all config files"))
        self.pB_SaveDefault.setText(_translate("PhyPiWindow", "Save Config"))
