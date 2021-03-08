from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin  # for parent ui to maya

ABOUT_SCRIPT = "\n" \
               "Latest updates:                          \n" \
               "                                         \n" \
               "08.02.2021   -add setting sever          \n" \
               "07.02.2021   -start refactoring          \n" \
               "                                         \n" \
               "Created by Andrey Belyaev                \n" \
               "andreikin@mail.ru"

HELP_TEXT = "\n" \
            "                Rename object script                                  .\n" \
            "- To rename object, enter the required name and click 'Rename'\n" \
            "- Selecting 'Rename hierarchy' button will rename all child objects.\n" \
            "- The button 'Select nonunic' will allow you to find objects in the \n" \
            "      scene that need to be renamed to prevent problems in the future." 
          

PREFFIX_LIST = ['none', 'l_', 'r_', 'up_', 'du_', 'fv_', 'bk_', 'lo_', 'mid_']
SUFFIX_LIST = ['none', '_geo', '_CT', '_jnt', '_grp', '_crv', '_clstr', '_loc']
DEFAULT_DIGITS = "##"
DEFAULT_SETTINGS = [0, "", DEFAULT_DIGITS, 1]

class MyWindow(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Rename object")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.setFixedSize(400, 130)
        
        # help and About script windows menu_bar
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)
        menu = QMenu("Edit")
        menuBar.addMenu(menu)        
        def_settings = QAction("Reset settings", self)
        menu.addAction(def_settings)        
        def_settings.triggered.connect(lambda:self.set_settings(*DEFAULT_SETTINGS))
        menu = QMenu("Help")
        menuBar.addMenu(menu)

        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(lambda:self.text_dialog("About program"))
        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(lambda:self.text_dialog("Help"))
        
        # line
        self.line = QFrame()  
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line)
        
        # Labels
        self.gridLayout = QGridLayout()
        self.layout.addLayout(self.gridLayout)
        self.label_pfx = QLabel(" Pfx:")  
        self.gridLayout.addWidget(self.label_pfx, 0, 0, 1, 1)
        self.label_name = QLabel(" Name:")
        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 1)
        self.label_digits = QLabel(" Digits:")
        self.gridLayout.addWidget(self.label_digits, 0, 2, 1, 1)
        self.label_sfx = QLabel(" Sfx:")
        self.gridLayout.addWidget(self.label_sfx, 0, 3, 1, 1)
        
        # comboBox_pfx, sfx, lineEdits
        self.comboBox_pfx = QComboBox()  
        for pfx in PREFFIX_LIST:
            self.comboBox_pfx.addItem(pfx)
        self.gridLayout.addWidget(self.comboBox_pfx, 1, 0, 1, 1)
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setMinimumSize(QSize(160, 20))
        self.gridLayout.addWidget(self.lineEdit_name, 1, 1, 1, 1)
        self.lineEdit_digit = QLineEdit()
        self.gridLayout.addWidget(self.lineEdit_digit, 1, 2, 1, 1)
        self.lineEdit_digit.setMinimumSize(QSize(30, 20))
        self.lineEdit_digit.setText(DEFAULT_DIGITS)
        self.comboBox_sfx = QComboBox()
        for sfx in SUFFIX_LIST:
            self.comboBox_sfx.addItem(sfx)
        self.gridLayout.addWidget(self.comboBox_sfx, 1, 3, 1, 1)

        self.line1 = QFrame()  # line
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line1)

        self.button_horizontalLayout = QHBoxLayout()  # buttons
        self.layout.addLayout(self.button_horizontalLayout)
        self.button_nonunik = QPushButton('Select nonunic')
        self.button_horizontalLayout.addWidget(self.button_nonunik)
        self.button_nonunik.clicked.connect(self.select_nonunic)
        self.button__hierarhy = QPushButton("Rename hierarchy")
        self.button_horizontalLayout.addWidget(self.button__hierarhy)
        self.button__hierarhy.clicked.connect(lambda: self.rename(True))
        self.button_rename = QPushButton("Rename")
        self.button_horizontalLayout.addWidget(self.button_rename)
        self.button_rename.clicked.connect(lambda: self.rename(False))
        
        # load settings
        self.settings = QSettings("anRename", "Settings")
        self.load_settings()
    
    def load_settings(self):
        """
        If settings not exist - load default settings
        """
        if self.settings.contains("renamer settings"):
            prefix, name, digs, suffix = self.settings.value("renamer settings")
        else:
            prefix, name, digs, suffix = DEFAULT_SETTINGS
        self.set_settings( prefix, name, digs, suffix)
        
    def set_settings(self, prefix, name, digs, suffix):
        self.comboBox_pfx.setCurrentIndex(int(prefix))
        self.lineEdit_name.setText(name)
        self.lineEdit_digit.setText(digs)
        self.comboBox_sfx.setCurrentIndex(int(suffix))        
        
         
    def closeEvent(self, evt):
        """
        When window closed it save fields settings
        """
        prefix = self.comboBox_pfx.currentIndex()
        name = self.lineEdit_name.text()
        digs = self.lineEdit_digit.text()
        suffix = self.comboBox_sfx.currentIndex()
        self.settings.setValue("renamer settings", [prefix, name, digs, suffix])
    
    
    def text_dialog(self, text_type):
        """
        Dialog window for help and about program
        """
        help_dialog = QMessageBox()
        help_dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        if text_type == "Help":
            help_dialog.setWindowTitle("Help window")
            help_dialog.setText(HELP_TEXT)
        else:
            help_dialog.setWindowTitle("About program")
            help_dialog.setText(ABOUT_SCRIPT)
        help_dialog.setStandardButtons(QMessageBox.Cancel)
        help_dialog.exec_()

    def rename(self, rename_hierarchy):
        prefix = self.__get_pfx_from_ui()
        new_name = self.__get_name_from_ui()
        digs = self.__get_digits_from_ui()
        suffix = self.__get_sfx_from_ui()
        sel = cmds.ls(selection=True)
        if not sel:
            raise ValueError('Must be selected at least one object.')
        else:
            node = cmds.createNode('unknown')
            cmds.addAttr(node, longName='selObjects', attributeType='message', multi=True, indexMatters=False)
            for each in sel:
                cmds.connectAttr('%s.message' % each, '%s.selObjects' % node, nextAvailable=True)
                if rename_hierarchy:
                    self.findChildren(each, node)
            con = cmds.listConnections('%s.selObjects' % node, source=True, destination=False)
            for i, obj in enumerate(con):
                num = i + 1
                objCurr = cmds.listConnections('%s.selObjects[%s]' % (node, i))[0]
                newDigs = (digs % num)
                result = prefix + new_name + newDigs + suffix
                cmds.select(objCurr, replace=True)
                result = cmds.rename(result)
            cmds.delete(node)
            cmds.select(clear=True)

    def select_nonunic(self):
        def isNameUnique(name):
            shortName = name.split("|")
            try:
                longNames = cmds.ls(shortName[-1], l=True)
            except:
                longNames = cmds.ls(("*" + shortName[-1]), l=True)
        
            if len(longNames) > 1:
                return 0
            else:
                return 1
                
        rez =[]
        for obj in cmds.ls():
            if not isNameUnique(obj):
                rez.append(obj)
        cmds.select(rez)
            
    def __get_pfx_from_ui(self):
        prefix = self.comboBox_pfx.currentText()
        if prefix == 'none':
            prefix = ''
        return prefix

    def __get_name_from_ui(self):
        return self.lineEdit_name.text()

    def __get_digits_from_ui(self):
        digits = self.lineEdit_digit.text()
        numDigits = digits.count('#')
        if numDigits == 0:
            raise ValueError("Count of # must be more then 0.")
        substr = '#' * numDigits
        zeroSubstr = '0' * numDigits
        newDig = digits.replace(substr, zeroSubstr)
        if newDig == digits:
            raise ValueError('Digits must contain only # symbols.')
        digs = digits.replace(substr, '%0' + str(numDigits) + 'd')
        return digs

    def __get_sfx_from_ui(self):
        suffix = self.comboBox_sfx.currentText()
        if suffix == 'none':
            suffix = ''
        return suffix

    def findChildren(self, parent, node):
        children = cmds.listRelatives(parent, children=True, fullPath=True)
        if children:
            for child in children:
                cmds.connectAttr('%s.message' % child, '%s.selObjects' % node, na=True)
                self.findChildren(child, node)


def rename_object():  
    global win
    try:
        win.deleteLater()
    except NameError as e:
        pass   
    win = MyWindow()
    win.show()

rename_object()



















