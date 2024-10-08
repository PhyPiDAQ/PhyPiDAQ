#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GUI to control run_phipy.py

- select and edit configuration files
- select working directory
- start data taking via execution of run_phypi.py
"""

from builtins import super
import os
import subprocess
import sys
import time
import yaml

from phypidaq._version_info import _get_version_string
from phypidaq.utils.path import get_user_home

from PyQt5.QtWidgets import QMessageBox

# Import all qt
import phypidaq.resources  # noqa: F401
from .phypiUi import *  # import code generated by designer-qt5

CONFIG_ENVIRONMENT_FILE = 'phypidaq.cfg'


# --> own implementation starts here -->
class PhyPiUiInterface(Ui_PhyPiWindow):
    """interface to class generated by designer-qt5"""

    def __init__(self, verbose: bool = True):
        # initialize configuration parameters
        self.config_directory = None
        self.work_directory_name = None
        # Parameter controlling verbose logging
        self.verbose = verbose

    def show_messagebox_question(self, title: str, text: str):
        # wrapper for QMessageBox Question yes/abort
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return msg.exec_()

    def show_messagebox_yes_no(self, title: str, text: str):
        # wrapper for QMessageBox Question yes/abort
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec_()

    def show_messagebox_info(self, title: str, text: str):
        # wrapper for QMessageBox Info
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec_()

    def show_messagebox_warning(self, title: str, text: str):
        # wrapper for QMessageBox Info
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec_()

    def init(self, window, daq_config_file, config_directory=None, work_directory_name=None):
        # Initialisation
        super().setupUi(window)  # initialize base class
        self.window = window
        # Update window title to include the current version of the software
        self.window.setWindowTitle(f"PhyPiDAQ [{_get_version_string()}]")

        # set display options, fonts etc.
        self.set_display_options()

        # set-up help
        self.set_help_en()

        # Find user config directory and create directory 'PhyPi'
        if config_directory is not None:
            # Check if the given path is absolute. This function is os-dependent.
            if os.path.isabs(config_directory):
                # Set the absolute path
                self.config_directory = config_directory
            else:
                # Make the relative path an absolute path
                self.config_directory = get_user_home() + os.sep + config_directory
                # Print some information when in verbose mode
                if self.verbose:
                    print(f"INFO: Absolute path to config directory is {self.config_directory}")
        else:
            # Set a config directory if no one is provided
            self.config_directory = get_user_home() + os.sep + 'PhyPi'
            if self.verbose:
                print(f"INFO: Setting config directory to {self.config_directory}")
        # Check if the config directory exists
        if not os.path.exists(self.config_directory):
            if self.verbose:
                print(f"INFO: Trying to create directory {self.config_directory}")
            try:
                os.makedirs(self.config_directory)
            except OSError:
                print("Could create config directory!")

        # set initial working Directory
        if work_directory_name is not None:
            # Check if this is an absolute path
            if os.path.isabs(work_directory_name):
                # Set the absolute path
                self.work_directory_name = work_directory_name
            else:
                # Use the given relative path to create the absolute path
                self.work_directory_name = get_user_home() + os.sep + work_directory_name
                # Print some information when in verbose mode
                if self.verbose:
                    print(f"INFO: Absolute path to working directory is {self.work_directory_name}")
        else:
            self.work_directory_name = self.config_directory
            if self.verbose:
                print(f"INFO: Setting working directory to {self.work_directory_name}")
        # Check if the given work directory exists
        if not os.path.exists(self.work_directory_name):
            if self.verbose:
                print(f"INFO: Trying to create directory {self.work_directory_name}")
            try:
                os.makedirs(self.work_directory_name)
            except OSError:
                print("Could create working directory!")

        self.lE_WorkDir.setText(self.work_directory_name)

        # set iterable over Device Configs Tabs (max. of 3)
        self.tab_DeviceConfigs = [self.tab_DeviceConfig0, self.tab_DeviceConfig1, self.tab_DeviceConfig2]
        self.pB_DeviceSelects = [self.pB_DeviceSelect0, self.pB_DeviceSelect1, self.pB_DeviceSelect2]
        self.pTE_DeviceConfigs = [self.pTE_DeviceConfig0, self.pTE_DeviceConfig1, self.pTE_DeviceConfig2]

        # define actions
        self.pB_abort.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.rB_EditMode.clicked.connect(self.actionEditConfig)
        self.pB_reloadConfig.clicked.connect(self.readDeviceConfig)
        self.pB_SaveDefault.clicked.connect(self.saveDefaultConfig)
        self.pB_FileSelect.clicked.connect(self.select_config_file)
        self.pB_DeviceSelect0.clicked.connect(self.select_device_file0)
        self.pB_DeviceSelect1.clicked.connect(self.select_device_file1)
        self.pB_DeviceSelect2.clicked.connect(self.select_device_file2)
        self.pB_WDselect.clicked.connect(self.selectWD)
        self.pB_Help.clicked.connect(self.set_help_en)
        self.pB_Hilfe.clicked.connect(self.set_help_de)
        self.pB_StartRun.clicked.connect(self.actionStartRun)

        # initialization dependent on DAQ config file
        self.init_daq(daq_config_file)

    def init_daq(self, daq_config_file):
        # initialize DAQ from config files - need absolute path
        path = os.path.dirname(daq_config_file)
        if path == '':
            path = '.'
        self.cwd = path

        try:
            with open(daq_config_file, 'r', encoding='utf-8') as f:
                DAQconf = f.read()
            # check if file is valid yaml format
            try:
                _confDict = yaml.load(DAQconf, Loader=yaml.Loader)
            except yaml.YAMLError as e:
                print('Exception: ', e)
                print('     DAQ configuration not valid yaml format' + daq_config_file)
                return

            # Do another file check
            if len(_confDict.keys()) == 0:
                print("Config dictionary is empty!")

        except OSError:
            print('Failed to read DAQ configuration file ' + daq_config_file)
            DAQconf = 'missing !'
            return

        self.lE_DAQConfFile.setText(daq_config_file)
        RunTag = os.path.split(daq_config_file)[1].split('.')[0]
        self.lE_RunTag.setText(RunTag)

        print('   - PhyPi configuration from file ' + daq_config_file)
        # display config data in GUI
        self.pTE_phypiConfig.setPlainText(DAQconf)

        # read device File(s) as specified in daq_config_file
        self.DeviceFiles = 3 * ['']
        self.readDeviceConfig()

    # - end initDAQ

    def set_display_options(self):
        # set font for plainTextEdit to monospace
        mono_font = QtGui.QFont()
        mono_font.setStyleHint(QtGui.QFont.TypeWriter)
        mono_font.setFamily("unexistentfont")
        self.pTE_phypiConfig.setFont(mono_font)
        self.pTE_DeviceConfig0.setFont(mono_font)
        self.pTE_DeviceConfig1.setFont(mono_font)
        # no line wrap, horizontal scroll bar instead
        self.pTE_phypiConfig.setLineWrapMode(0)
        self.pTE_DeviceConfig0.setLineWrapMode(0)
        self.pTE_DeviceConfig1.setLineWrapMode(0)

    def set_help_de(self):
        try:
            self.TE_Help.setText(open('doc/Hilfe.html', 'r', encoding='utf-8').read())
        except OSError:
            self.TE_Help.setText("Fehlt!")

    def set_help_en(self):
        try:
            self.TE_Help.setText(open('doc/Help.html', 'r', encoding='utf-8').read())
        except OSError:
            self.TE_Help.setText("Missing!")

    def setDevConfig_fromFile(self, i, fname):
        try:
            self.pTE_DeviceConfigs[i].setPlainText(open(fname).read())
            print('   - Device configuration from file ' + fname)
        except OSError:
            self.pTE_DeviceConfigs[i].setPlainText('# no config file ' + fname)

    def readDeviceConfig(self):
        #   read Device Configuration as specified by actual phypi DAQ config
        try:
            phypiConfD = yaml.load(self.pTE_phypiConfig.toPlainText(), Loader=yaml.Loader)
        except yaml.YAMLError:
            print('DAQ configuration not valid yaml format!')
            return

        # find the device configuration file
        if "DeviceFile" in phypiConfD:
            DevFiles = phypiConfD["DeviceFile"]
        elif "DAQModule" in phypiConfD:
            DevFiles = phypiConfD["DAQModule"] + '.yaml'
        else:
            print('     no device configuration file given')
            # exit(1)
            return

        # if not a list, make it one
        if not isinstance(DevFiles, list):
            DevFiles = [DevFiles]
        self.NDeviceConfigs = len(DevFiles)
        #  enable Config Tabs if needed
        _translate = QtCore.QCoreApplication.translate
        for i in range(1, self.NDeviceConfigs):
            self.tab_DeviceConfigs[i].setEnabled(True)
            self.tabConfig.setTabText(
                self.tabConfig.indexOf(self.tab_DeviceConfigs[i]),
                _translate("PhyPiWindow", "Device Config " + str(i + 1)),
            )

        for i in range(self.NDeviceConfigs, len(self.tab_DeviceConfigs)):
            self.tab_DeviceConfigs[i].setEnabled(False)
            self.tabConfig.setTabText(self.tabConfig.indexOf(self.tab_DeviceConfigs[i]), _translate("PhyPiWindow", ""))

            # (re-)read device config if file name in phypi Config changed
        for i, DevFnam in enumerate(DevFiles):
            if DevFnam != self.DeviceFiles[i]:
                fname = self.cwd + os.sep + DevFnam
                self.setDevConfig_fromFile(i, fname)
                if self.DeviceFiles[i] != '':
                    self.show_messagebox_info('Info', 'Device Configuration re-read, please check')
                self.DeviceFiles[i] = DevFiles[i]

    def get_file(self, file_description: str, file_directory: str, file_type: str):
        # Check the passed parameters to the function
        if file_description is None or file_type is None or file_directory is None:
            raise AttributeError("File dialog parameter's can't be empty!")
        # Open a file open dialog
        file_paths = QtWidgets.QFileDialog.getOpenFileName(None, file_description, file_directory, file_type)
        if len(file_paths) > 1:
            # Return the path to the first file which was selected
            file_name = str(file_paths[0]).strip()
            return file_name
        else:
            # If no file is selected, return an empty string
            return ""

    def select_config_file(self):
        file_name = self.get_file('PhyPi config', self.config_directory, 'DAQ(*.daq)')
        if file_name != '':
            # print('selected File ' + str(FileName) )
            # remember new config directory
            self.config_directory = os.path.dirname(file_name)
            self.init_daq(file_name)

    def select_device_file0(self):
        file_name = self.get_file('Device config', self.config_directory, 'yaml(*.yaml)')
        if file_name != '':
            # print('selected File ' + str(FileName) )
            self.setDevConfig_fromFile(0, file_name)

    def select_device_file1(self):
        file_name = self.get_file('Device config', self.config_directory, 'yaml(*.yaml)')
        if file_name != '':
            # print('selected File ' + str(FileName) )
            self.setDevConfig_fromFile(1, file_name)

    def select_device_file2(self):
        file_name = self.get_file('Device config', self.config_directory, 'yaml(*.yaml)')
        if file_name != '':
            # print('selected File ' + str(FileName) )
            self.setDevConfig_fromFile(2, file_name)

    def selectWD(self):
        path2WD = QtWidgets.QFileDialog.getExistingDirectory(None, '~')
        WDname = str(path2WD).strip()
        if WDname != '':
            # print('selected Directory' + WDname )
            self.lE_WorkDir.setText(WDname)
            self.work_directory_name = WDname

    def actionEditConfig(self):
        checked = self.rB_EditMode.isChecked()
        self.pTE_phypiConfig.setReadOnly(not checked)
        self.pB_reloadConfig.setEnabled(checked)
        self.pTE_DeviceConfig0.setReadOnly(not checked)
        self.pTE_DeviceConfig1.setReadOnly(not checked)
        self.pTE_DeviceConfig2.setReadOnly(not checked)

    def saveConfigs(self, config_directory, DAQfile=None, verbose=0):
        # save all Config files to config_directory

        # retrieve actual configuration from GUI
        DAQconf = self.pTE_phypiConfig.toPlainText()
        # check validity of configuration files for valid yaml syntax
        try:
            DAQconfdict = yaml.load(DAQconf, Loader=yaml.Loader)
        except yaml.YAMLError as e:
            self.show_messagebox_warning('Warning', 'PhyPi Config is not valid yaml format \n' + str(e))
            return 1

        DevConfs = []
        for i in range(self.NDeviceConfigs):
            DevConfs.append(self.pTE_DeviceConfigs[i].toPlainText())
            try:
                _ = yaml.load(DevConfs[i], Loader=yaml.Loader)
            except yaml.YAMLError as e:
                self.show_messagebox_warning('Warning', 'Device Config %i is not valid yaml format \n' % i + str(e))
                return 1

        # name of DAQ configuration file in config_directory
        if DAQfile is None:  # derive from RunTag if not given
            DAQfile = str(self.lE_RunTag.text()).replace(' ', '') + '.daq'
        fullDAQfile = config_directory + os.sep + DAQfile

        if verbose:
            if self.show_messagebox_question('Question', 'saving Config to file ' + fullDAQfile) == QMessageBox.Cancel:
                return 1

        DevFiles = DAQconfdict["DeviceFile"]
        if not isinstance(DevFiles, list):
            DevFiles = [DevFiles]

        # check for overwriting ...
        #   ... device config files
        for DevFile in DevFiles:
            fullDevFile = config_directory + os.sep + DevFile
            if os.path.isfile(fullDevFile):
                if (
                    self.show_messagebox_question('Question', 'File ' + fullDevFile + ' exists - overwrite ?')
                    == QMessageBox.Cancel
                ):
                    return 1
        #  ... DAQ file
        if os.path.isfile(fullDAQfile):
            if (
                self.show_messagebox_question('Question', 'File ' + fullDAQfile + ' exists - overwrite ?')
                == QMessageBox.Cancel
            ):
                return 1

        # if ok, write all files
        try:
            fDAQ = open(fullDAQfile, 'w')
            print(DAQconf, file=fDAQ)
            self.DAQfile = DAQfile
            fDAQ.close()
            print('   - saved PhyPy configuration to ' + fullDAQfile)
        except Exception as e:
            self.show_messagebox_warning("Warning", 'Failed to store ' + fullDAQfile + '\n' + str(e))
            return 1

        for i, DevFile in enumerate(DevFiles):
            cdir, fnam = os.path.split(DevFile)
            # make subdirectory if needed and non-existent
            if cdir != '':
                if not os.path.exists(config_directory + os.sep + cdir):
                    try:
                        os.makedirs(config_directory + os.sep + cdir)
                    except OSError:
                        print(f"Couldn't create folder {cdir}!")
            fDev = open(config_directory + os.sep + DevFile, 'w')
            print(DevConfs[i], file=fDev)
            fDev.close()
            print('   - saved Device configuration to ' + fullDevFile)

        if verbose:
            self.show_messagebox_info('Info', 'saved PhyPi and Device Configuration')
        return 0

    def saveDefaultConfig(self):
        # save configuration
        # propose name for DAQ configuration file from RunTag
        _file = self.config_directory + os.sep + str(self.lE_RunTag.text()).replace(' ', '') + '.daq'
        # select file and directory
        path2File = QtWidgets.QFileDialog.getSaveFileName(None, 'save configuration as', _file, 'daq(*.daq)')
        fullDAQfile = str(path2File[0]).strip()
        if fullDAQfile != '':
            # remember new config directory
            self.config_directory = os.path.dirname(fullDAQfile)
            DAQfile = os.path.basename(fullDAQfile)
        else:
            print("   abort - no file name given")
            return 1
        # set name and save all configs
        self.lE_DAQConfFile.setText(fullDAQfile)
        if self.saveConfigs(self.config_directory, DAQfile=DAQfile, verbose=0):
            print("   !!! failed to save configuration files")
            return 1
        else:
            print("   - configuration files stored in directory " + self.config_directory)
            return 0

    def saveEnvironment(self):
        """Save PhyPi configuration to file ~/CONFIG_ENVIRONMENT_FILE"""
        # ... and find name of work directory
        config_name = get_user_home() + os.sep + CONFIG_ENVIRONMENT_FILE
        fcfg = open(config_name, 'w')
        print('work_directory: ', self.work_directory_name, file=fcfg)
        print('config_directory: ', self.config_directory, file=fcfg)
        print('daq_file: ', os.path.basename(self.DAQfile), file=fcfg)

    def actionStartRun(self):
        # start script run_phipy in subdirectory

        # generate a dedicated subdirectory
        datetime = time.strftime('%y%m%d-%H%M', time.localtime())
        RunTag = ''.join(str(self.lE_RunTag.text()).split())
        self.runDir = RunTag + '_' + datetime  # timestamp
        self.path_to_WD = self.work_directory_name + os.sep + self.runDir
        if not os.path.exists(self.path_to_WD):
            try:
                os.makedirs(self.path_to_WD)
            except OSError:
                print("Couldn't create folder!")

        if self.saveConfigs(self.path_to_WD):
            return
        print("   - files for this run stored in directory " + self.path_to_WD)

        # save changes to phypidaq configuration
        self.saveEnvironment()

        # close GUI window and start runCosmo
        print('\n*==* PhyPi Gui: closing window and starting run_phypi.py')
        self.window.hide()

        # start script
        self.start_runphypi()

        # exit or continue ?
        if self.show_messagebox_yes_no('End Dialog', 'Exit phypi ? ') == QMessageBox.Yes:
            QtCore.QCoreApplication.instance().quit()
            print('*==* phypi: exit \n')
        else:
            self.window.show()

    def start_runphypi(self):
        subprocess.run(args=[sys.executable, "-m", "phypidaq.runPhyPiDAQ", self.DAQfile], cwd=self.path_to_WD)


# - end Class Ui_PhyPiWindow


def run_phypi_ui():
    script = sys.argv[0]
    # Print the script path
    print(f"\n*==* {script} running")

    # Get relevant paths
    # Get that of the currently executed python file
    path_to_phypi = os.path.dirname(script)
    # Get the user home path
    homedir = get_user_home()
    # Try finding the path of the config file
    config_name = homedir + os.sep + CONFIG_ENVIRONMENT_FILE
    # Try reading and parsing the config file
    try:
        # Try opening a possible config file in the home path
        with open(config_name) as config:
            # Try reading the config fiel
            config_dict = yaml.load(config, Loader=yaml.Loader)
    except (OSError, yaml.YAMLError):
        # If the first step failed, try opening a possible config file in the path of PhyPiDAQ
        config_name = path_to_phypi + os.sep + CONFIG_ENVIRONMENT_FILE
        try:
            with open(config_name) as config:
                config_dict = yaml.load(config, Loader=yaml.Loader)
        except (OSError, yaml.YAMLError):
            # Couldn't find any config files
            print(f"Warning: No valid file {CONFIG_ENVIRONMENT_FILE} found - using defaults")
            # Set up a config directory with the default values. Use the platform defaults for home directory as work
            # directory (which is the absolute path of '~' on Linux and the USERPROFILE-variable on Windows)
            config_dict = {'work_directory': get_user_home(), 'config_directory': ' ', 'daq_file': 'PhyPiDemo.daq'}

    # Try getting the work directory
    work_directory = config_dict['work_directory']
    if work_directory == '~':
        work_directory = homedir
    if work_directory == '.':
        work_directory = os.getcwd()
    # Try getting the config directory
    conf_directory = config_dict['config_directory']
    if conf_directory == '~':
        conf_directory = homedir
    if conf_directory == '.':
        conf_directory = os.getcwd()
    if conf_directory == ' ':
        conf_directory = path_to_phypi
    # Try getting the path of the data acquisition config file
    daq_config_file = conf_directory + os.sep + config_dict['daq_file']

    # Check for/read command line arguments and get DAQ configuration file
    if len(sys.argv) == 2:
        if sys.argv[1].strip() != '':
            daq_config_file = os.path.abspath(sys.argv[1])  # with full path to file
            conf_directory = os.path.dirname(daq_config_file)  # config dir from file name

    # Print config information
    print(f"     work directory: {work_directory}")
    print(f"     configuration directory: {conf_directory}")
    print(f"     DAQ configuration file: {daq_config_file}")

    # start GUI
    if path_to_phypi != '':
        os.chdir(path_to_phypi)  # change path to where PhyPi lives
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    # call custom implementation
    ui = PhyPiUiInterface()
    ui.init(main_window, daq_config_file, config_directory=conf_directory, work_directory_name=work_directory)

    # start pyqt event loop
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":  # - - - - - - - - - - - - - - - - - - - -
    run_phypi_ui()
