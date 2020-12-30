from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functools import partial
import maya.cmds as cmds


def conf(data_type):
    data = {
        "prefixList": ['none',
                       'l_',
                       'r_',
                       'up_',
                       'fv_',
                       'bk_',
                       'lo_',
                       'mid_'],
        "suffixList": ['none',
                       '_CT',
                       '_bind',
                       '_jnt',
                       '_geo',
                       '_grp',
                       '_crv',
                       '_clstr',
                       '_loc',
                       '_mdv',
                       '_pma',
                       '_uc',
                       '_mdl',
                       '_adl']
    }
    return data[data_type]


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # Window settings
        self.setFixedWidth(358)
        self.setFixedHeight(100)

        self.layout = QVBoxLayout()  # Layouts settings
        self.setLayout(self.layout)
        self.gridLayout = QGridLayout()
        self.layout.addLayout(self.gridLayout)

        self.label_pfx = QLabel("Pfx:")  # Labels
        self.gridLayout.addWidget(self.label_pfx, 0, 0, 1, 1)
        self.label_name = QLabel("Name:")
        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 1)
        self.label_digits = QLabel("Digits:")
        self.gridLayout.addWidget(self.label_digits, 0, 2, 1, 1)
        self.label_sfx = QLabel("Sfx:")
        self.gridLayout.addWidget(self.label_sfx, 0, 3, 1, 1)

        self.comboBox_pfx = QComboBox()  # comboBox_pfx, sfx, lineEdits
        for pfx in conf("prefixList"):
            self.comboBox_pfx.addItem(pfx)
        self.gridLayout.addWidget(self.comboBox_pfx, 1, 0, 1, 1)
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setMinimumSize(QSize(150, 0))
        self.gridLayout.addWidget(self.lineEdit_name, 1, 1, 1, 1)
        self.lineEdit_digit = QLineEdit()
        self.gridLayout.addWidget(self.lineEdit_digit, 1, 2, 1, 1)
        self.lineEdit_digit.setMaximumSize(QSize(50, 20))
        self.lineEdit_digit.setText("##")
        self.comboBox_sfx = QComboBox()
        for sfx in conf("suffixList"):
            self.comboBox_sfx.addItem(sfx)
        self.gridLayout.addWidget(self.comboBox_sfx, 1, 3, 1, 1)

        self.line = QFrame()  # line
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line)

        self.button_horizontalLayout = QHBoxLayout()  # buttons
        self.layout.addLayout(self.button_horizontalLayout)
        self.button_nonunik = QPushButton('Select nonunic')
        self.button_horizontalLayout.addWidget(self.button_nonunik)
        self.button_nonunik.clicked.connect(self.select_nonunic)
        self.button__hierarhy = QPushButton("Rename hierarchy")
        self.button_horizontalLayout.addWidget(self.button__hierarhy)
        self.button__hierarhy.clicked.connect(partial(self.rename, True))
        self.button_rename = QPushButton("Rename")
        self.button_horizontalLayout.addWidget(self.button_rename)
        self.button_rename.clicked.connect(partial(self.rename, False))

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
                    self.pvFindChildren(each, node)
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

    def pvFindChildren(self, parent, node):
        children = cmds.listRelatives(parent, children=True, fullPath=True)
        if children:
            for child in children:
                cmds.connectAttr('%s.message' % child, '%s.selObjects' % node, na=True)
                self.pvFindChildren(child, node)





def pvRename():  
    global win
    try:
        win.deleteLater()
    except NameError as e:
        pass   
    win = MyWindow()
    win.show()


pvRename()



















