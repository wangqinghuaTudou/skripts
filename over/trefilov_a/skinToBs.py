import sys, sip
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as omui
import maya.mel as mel
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sets import Set
from pvDuplicateDefault import * 

def skinToBs(skinName = None, bsName = None, keyframeJoints = None, ui = False):
    """Convert skinning to blendshape geometry
    
    Args:
        skinName (str): skinning geometry name (input name)
        bsName (str): blendshape geometry name (output name)
        keyframeJoints (dict): joints with keyframes
        ui (bool): user interface
        
    Returns:
        int: 0 = success, 1 = failure, 2 = ui invoked
    
    Examples:
        Auto converting
        skinToBs()
        
        Convert skinning 'pCylinder1' to blendshape geometry 'bs_pCylinder1' by joint 'joint1' with keyframes 60, 94 and joint 'joint2' with keyframes 24, 36, 50
        skinToBs('pCylinder1', 'bs_pCylinder1', { 'joint1': [60, 94], 'joint2': [24, 36, 50] } )
        
        Invoke UI
        skinToBs(ui = True)

        Invoke UI and fill appropriate fields
        skinToBs('pCylinder1', 'bs_pCylinder1', { 'joint1': [60, 94], 'joint2': [24, 36, 50] }, ui = True)"""
        
    if ui:
        skinToBsUi = SkinToBsUi(skinName, bsName, keyframeJoints)
        skinToBsUi.show()
        return 2
    
    if not skinName:
        selection = cmds.ls(sl = True, tl = 1)
        if selection:
            skinName = selection[0]
        else:
            print "skinToBs(): object is not specified"
            return 1
            
    if not bsName:
        bsName = "bs_" + skinName    
    
    if not keyframeJoints:
        keyframeJoints = getKeyframeJoints(skinName)
            
    keyframeFound = False
    for value in keyframeJoints.values():
        if value:
            keyframeFound = True
            break
        
    if not keyframeFound:
        print "skinToBs(): can't find joints with keyframes"
        return 1
         
    try:
        duplicates = pvDuplicateDefault(skinName)
    except:
        print "skinToBs(): can't create duplicate of '{}'".format(skinName)
        return 1

    if not duplicates:
        print "skinToBs(): duplicates' list is empty"
        return 1            
            
    newName = cmds.rename(duplicates[0], bsName)
    if newName == duplicates[0]:
        print "skinToBs(): fail to rename duplicate from '{}' to '{}'".format(newName, bsName)
        cmds.delete(duplicates[0])
        return 1

    blendshape = cmds.blendShape(bsName)
    if not blendshape:
        print "skinToBs(): can't add blendshape to '{}'".format(bsName)
        cmds.delete(bsName)
        return 1
            
    index = 0
    curTime = cmds.currentTime(q = True)
    for jointName, keyframes in keyframeJoints.items():
        for keyFrame in keyframes:
            cmds.currentTime(keyFrame, e = True)
            
            dup = cmds.duplicate(skinName)
            if not dup:
                print "skinToBs(): can't create duplicate of '{}'".format(skinName)
                cmds.delete(bsName)
                return 1
                
            cmds.blendShape(blendshape[0], e = True, t = (bsName, index, dup[0], 1.0))
            cmds.delete(dup[0])
            index += 1
        
    cmds.currentTime(curTime, e = True)
        
    return 0
        
def getKeyframeJoints(name):
    keyframeJoints = {}
    if not name:
        print "getKeyframeJoints(str): object name is not specified"
        return keyframeJoints

    skinClust = None
    try:
        skinClust = mel.eval('findRelatedSkinCluster ' + name)
    finally:
        if not skinClust:
            print "getKeyframeJoints(str): cant't find skinCluster of object '{}' ".format(name)
            return keyframeJoints

    joints = cmds.skinCluster(skinClust, q = True, inf = True)
    if not joints:
        print "getKeyframeJoints(str): can't find joints of skinCluster '{}'".format(skinClust)
        return keyframeJoints

    for jointName in joints:
        keyframes = cmds.keyframe(jointName, q = True)
        if keyframes:
            keyframeJoints[jointName] = sorted(list(set(keyframes)));
        else:    
            keyframeJoints[jointName] = [];

    return keyframeJoints;
    
def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QObject)
    
class SkinToBsUi(QWidget):
    def __init__(self, skinName = None, bsName = None, keyframeJoints = None, parent = getMayaWindow()):
        super(SkinToBsUi, self).__init__(parent)
        self.setMinimumWidth(350)
        self.setWindowTitle("Convert skinning to blendshape")
        self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.setupUi()
        self.initialize(skinName, bsName, keyframeJoints)
    
    def setupUi(self):
        self.mainLayout = QGridLayout(self)
        self.setLayout(self.mainLayout)
        
        skinnedGeoLabel = QLabel("Skinned Geo", self)
        skinnedGeoLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.mainLayout.addWidget(skinnedGeoLabel, 0, 0, 1, 1)
        
        skinnedGeoButton = QPushButton("<<", self)
        skinnedGeoButton.clicked.connect(self.getSelectedMayaObj)
        skinnedGeoButton.setToolTip("Import name of selected maya object")
        skinnedGeoButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.mainLayout.addWidget(skinnedGeoButton, 0, 1, 1, 1, Qt.AlignRight)
        
        self.skinnedGeoEdit = QLineEdit(self)
        self.skinnedGeoEdit.textChanged.connect(self.skinnedGeoTextChanged)
        self.skinnedGeoEdit.setValidator(QRegExpValidator(QRegExp("^\D.*")))
        self.mainLayout.addWidget(self.skinnedGeoEdit, 1, 0, 1, 2)
        
        self.mainLayout.addItem(QSpacerItem(1, 10, QSizePolicy.Preferred, QSizePolicy.Fixed))
        
        blendshapeGeoLabel = QLabel("Blendshape Geo", self)
        self.mainLayout.addWidget(blendshapeGeoLabel, 3, 0, 1, 2)
        
        self.blendshapeGeoEdit = QLineEdit(self)
        self.blendshapeGeoEdit.textChanged.connect(self.blendshapeGeoTextChanged)
        self.mainLayout.addWidget(self.blendshapeGeoEdit, 4, 0, 1, 2)
        
        self.mainLayout.addItem(QSpacerItem(1, 10, QSizePolicy.Preferred, QSizePolicy.Fixed))
        
        definingKeyFramesLabel = QLabel("Keyframes Defining", self)
        self.mainLayout.addWidget(definingKeyFramesLabel, 6, 0, 1, 2)
        
        self.autoKeyFramesButton = QRadioButton("Auto", self)
        self.autoKeyFramesButton.setChecked(True)
        self.mainLayout.addWidget(self.autoKeyFramesButton, 7, 0, 1, 1)
        
        self.manualKeyFramesButton = QRadioButton("Manual", self)
        self.mainLayout.addWidget(self.manualKeyFramesButton, 7, 1, 1, 1)
        
        self.jointsList = QTreeWidget(self)
        self.jointsList.setSelectionMode(QTreeWidget.NoSelection)
        self.jointsList.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.jointsList.setStyleSheet("* QCheckBox:disabled { color: rgb(240, 120, 120); } ")
        self.autoKeyFramesButton.clicked.connect(self.jointsList.hide)
        self.manualKeyFramesButton.clicked.connect(self.jointsList.show)
        self.mainLayout.addWidget(self.jointsList, 8, 0, 1, 2, )
        self.mainLayout.setRowStretch(8, 1)
        self.jointsList.header().hide()
        self.jointsList.hide()
        
        self.mainLayout.addItem(QSpacerItem(1, 9, QSizePolicy.Preferred, QSizePolicy.Expanding))
        
        self.runButton = QPushButton("Run", self)
        self.runButton.clicked.connect(self.runButtonClicked)
        self.mainLayout.addWidget(self.runButton, 10, 0, 1, 2)
        self.runButton.setDisabled(True)
        
        self.errorMsg = QLabel(self)
        self.errorMsg.setStyleSheet(
            """* { 
                border-radius: 2px;
                border: 1px solid red;
                background: rgb(140, 40, 40);
            }"""
        );
        self.errorMsg.setFixedHeight(25)
        self.errorMsg.hide()
        
        self.infoMsgs = InfoMessagesWt(self)
        self.infoMsgs.errorsFound.connect(self.runButton.setDisabled)
        self.mainLayout.addWidget(self.infoMsgs, 11, 0, 1, 2, Qt.AlignBottom)
        
    def initialize(self, skinName, bsName, keyframeJoints):
        if skinName:
            self.skinnedGeoEdit.setText(skinName)
            
        if bsName:
            self.blendshapeGeoEdit.setText(bsName)
                        
        if keyframeJoints:
            self.manualKeyFramesButton.click()
            self.loadJoints(keyframeJoints)
        
    def getSelectedMayaObj(self):
        selections = cmds.ls(selection = True, tail = 1)
        if selections:
            self.skinnedGeoEdit.setText(selections[0])
        else:
            self.skinnedGeoEdit.clear()
            
    def skinnedGeoTextChanged(self, text):
        self.loadJoints()
        if text:
            objects = cmds.ls(text)
            if objects:
                self.infoMsgs.removeMsg(self.skinnedGeoEdit, "Can't find typed skinned geometry")
                self.blendshapeGeoEdit.setText("bs_" + text)
            else:
                self.infoMsgs.addMsg(self.skinnedGeoEdit, "Can't find typed skinned geometry", 0)
        else:
            self.blendshapeGeoEdit.clear()
            
    def blendshapeGeoTextChanged(self, text):
        objects = cmds.ls(text)
        if objects:
            self.infoMsgs.addMsg(self.blendshapeGeoEdit, "Such blendshape geometry already exists", 0)
        else:
            self.infoMsgs.removeMsg(self.blendshapeGeoEdit, "Such blendshape geometry already exists")
            
    def loadJoints(self, keyframeJoints = None):
        self.jointsList.clear()
        
        if not keyframeJoints:
            keyframeJoints = getKeyframeJoints(self.skinnedGeoEdit.text())
        
        for jointName, keyframes in keyframeJoints.items():
            jointItem = QTreeWidgetItem()
            self.jointsList.addTopLevelItem(jointItem)
            
            jointBox = QCheckBox(self.jointsList)
            jointBox.setText(jointName)
            jointBox.setMinimumHeight(25)
            self.jointsList.setItemWidget(jointItem, 0, jointBox)
            
            if keyframes:
                jointBox.setChecked(True)
                    
                keyframeItem = QTreeWidgetItem()
                jointItem.addChild(keyframeItem)
                    
                keyframesList = KeyframesList(keyframes, self)
                self.jointsList.setItemWidget(keyframeItem, 0, keyframesList)
            else:
                jointBox.setText(jointBox.text() + " (keyframes not found)")
                jointBox.setDisabled(True)
            
    def showErrorMsg(self, obj, text):
        pos = self.mapTo(self, obj.geometry().bottomLeft())
        self.errorMsg.setText(text)
        self.errorMsg.setFixedWidth(self.width() - self.mainLayout.contentsMargins().left() - self.mainLayout.contentsMargins().right())
        self.errorMsg.move(pos)
        self.errorMsg.show()
        self.runButton.setDisabled(True)
            
    def hideErrorMsg(self):
        self.errorMsg.hide()
        self.runButton.setEnabled(True)
               
    def runButtonClicked(self):
        keyframeJoints = {}
        if self.autoKeyFramesButton.isChecked():
            keyframeJoints = getKeyframeJoints(self.skinnedGeoEdit.text())
        else:
            for i in range(self.jointsList.topLevelItemCount()):
                jointItem = self.jointsList.topLevelItem(i)
                if not jointItem:
                    continue
                            
                jointBox = self.jointsList.itemWidget(jointItem, 0)
                if not jointBox:
                    continue
                            
                if not jointBox.isChecked():
                    continue
                            
                keyframesItem = jointItem.child(0)
                if not keyframesItem:
                    continue
                            
                keyframesList = self.jointsList.itemWidget(keyframesItem, 0)
                if not keyframesList:
                    continue
                            
                keyframeJoints[jointBox.text()] = keyframesList.getKeyframes()
        skinToBs(self.skinnedGeoEdit.text(), self.blendshapeGeoEdit.text(), keyframeJoints)

class KeyframesList(QListWidget):
    def __init__(self, keyframes, parent = None):
        super(KeyframesList, self).__init__(parent);
        self.keyframeWts = {};
        self.setupUi();
        self.initialize(keyframes);
 
    def setupUi(self):
        self.setSpacing(1);
        self.setResizeMode(QListView.Adjust);
        self.setSelectionMode(QListWidget.NoSelection);
        
        item = QListWidgetItem();
        self.addItem(item);

        addWidget = QWidget(self);
        addLayout = QHBoxLayout(addWidget);
        addLayout.setContentsMargins(0, 0, 0, 0);
        addWidget.setLayout(addLayout);
        
        addButton = QPushButton("Add", addWidget);
        addButton.setFixedWidth(50);
        addButton.clicked.connect(self.addRowClicked);
        addLayout.addWidget(addButton, 0, Qt.AlignRight);
        
        self.setItemWidget(item, addWidget);
        item.setSizeHint(addWidget.sizeHint());
        
    def initialize(self, keyframes):
        if keyframes:
            for keyFrame in keyframes:
                self.addKeyframe(keyFrame);
        else:
            self.list.hide();
            
    def addKeyframe(self, keyFrame):
        item = QListWidgetItem();
        self.insertItem(self.count() - 1, item);
        
        keyframeWt = KeyframeWt(keyFrame, self);
        keyframeWt.removed.connect(self.removeKeyFrame);
        self.setItemWidget(item, keyframeWt);
        
        item.setSizeHint(keyframeWt.sizeHint());
        self.keyframeWts[keyframeWt] = item;
        
    def removeKeyFrame(self):
        item = self.keyframeWts.pop(self.sender());
        self.takeItem(self.row(item));
        
    def getKeyframes(self):
        keyframes = []
        for keyframeWt in self.keyframeWts.keys():
            keyframes.append(keyframeWt.keyframeBox.value())
        return keyframes

    def sizeHint(self):
        rowHeight = 0;
        item = self.item(0);
        if item:
            rowHeight = item.sizeHint().height();
        return QSize(self.width(), self.count() * (rowHeight + 2 * self.spacing()) + 2 * self.frameWidth());
        
    def addRowClicked(self):
        self.addKeyframe(0);
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum());
        
class KeyframeWt(QWidget):
    removed = pyqtSignal()
    
    def __init__(self, number, parent = None):
        super(KeyframeWt, self).__init__(parent)
        self.setupUi()
        self.keyframeBox.setValue(number)
        
    def setupUi(self):
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)
        
        keyframeLabel = QLabel("keyframe", self)
        mainLayout.addWidget(keyframeLabel)
        
        self.keyframeBox = QSpinBox(self)
        self.keyframeBox.setRange(0, sys.maxint)
        self.keyframeBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.keyframeBox.valueChanged.connect(self.keyframeChanged)
        mainLayout.addWidget(self.keyframeBox)
        
        importKeyframeButton = QPushButton("<<", self)
        importKeyframeButton.setToolTip("Import keyframe from scene")
        importKeyframeButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        importKeyframeButton.clicked.connect(self.importKeframeButtonClicked)
        mainLayout.addWidget(importKeyframeButton)
        
        self.removeKeyframeButton = QPushButton(self)
        self.removeKeyframeButton.setFixedWidth(50)
        self.removeKeyframeButton.setText("Remove")
        self.removeKeyframeButton.clicked.connect(self.removeKeyframeButtonClicked)
        mainLayout.addWidget(self.removeKeyframeButton)

    def removeKeyframeButtonClicked(self):
        skinToBsUi = self.getSkinToBsUi()
        if skinToBsUi:
            skinToBsUi.infoMsgs.removeMsg(self)
            
        self.removed.emit()
        
    def importKeframeButtonClicked(self):
        curTime = cmds.currentTime(q = True)
        self.keyframeBox.setValue(curTime)
                
    def keyframeChanged(self, value):
        skinToBsUi = self.getSkinToBsUi()
        if not skinToBsUi:
            return

        jointsList = skinToBsUi.jointsList
        keyframesItem = jointsList.itemAt(QCursor.pos() - jointsList.mapToGlobal(QPoint(0, 0)))
        if not keyframesItem:
            return
            
        jointItem = keyframesItem.parent()
        if not jointItem:
            return
            
        jointBox = jointsList.itemWidget(jointItem, 0)
        if not jointBox:
            return
           
        curKeyframe = cmds.keyframe(jointBox.text(), q = True, time = (value, value))
        skinToBsUi.infoMsgs.removeMsg(self)
        if not curKeyframe:
            skinToBsUi.infoMsgs.addMsg(self, "{} is not keyframe of joint '{}'".format(value, jointBox.text()), 1)
            
    def getSkinToBsUi(self):
        skinToBsUi = None
        tmp = self.parentWidget()
        while tmp:
            if type(tmp).__name__ == 'SkinToBsUi':
                skinToBsUi = tmp
                break
            else:
                tmp = tmp.parentWidget()
        return skinToBsUi
                
class InfoMessagesWt(QWidget):
    errorsFound = pyqtSignal(bool)
    
    def __init__(self, parent = None):
        super(InfoMessagesWt, self).__init__(parent)
        self.messages = {}
        self.setupUi()
        
    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)
        
        panelLayout = QHBoxLayout(self)
        panelLayout.setSpacing(0)
        panelLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(panelLayout)
        
        self.expandButton = QToolButton(self)
        self.expandButton.setStyleSheet("QToolButton { border: none }")
        self.expandButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.expandButton.setArrowType(Qt.RightArrow)
        self.expandButton.setCheckable(True)
        self.expandButton.setChecked(False)
        self.expandButton.toggled.connect(self.expandButtonClicked)
        self.expandButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        panelLayout.addWidget(self.expandButton)
        
        self.errorsCounter = QToolButton(self)
        self.errorsCounter.setText("errors: 0")
        self.errorsCounter.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.errorsCounter.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxCritical))
        self.errorsCounter.setIconSize(QSize(10, 10))
        panelLayout.addWidget(self.errorsCounter)
        
        self.warningsCounter = QToolButton(self)
        self.warningsCounter.setText("warnings: 0")
        self.warningsCounter.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.warningsCounter.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))
        self.warningsCounter.setIconSize(QSize(10, 10))
        panelLayout.addWidget(self.warningsCounter)
        
        panelLayout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Preferred))
        
        self.contentWt = QWidget(self)
        self.mainLayout.addWidget(self.contentWt)
        self.contentWt.hide()
        
        self.contentLayout = QVBoxLayout(self)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentWt.setLayout(self.contentLayout)
        
    def expandButtonClicked(self, on):
        self.expandButton.setArrowType(Qt.DownArrow if on else Qt.RightArrow)
        self.contentWt.setVisible(on)
        
    def addMsg(self, wt, text, type):
        msgExists = False
        for key, value in self.messages.iteritems():
            if key.text() == text and value == wt:
                msgExists = True
                break
        
        if not msgExists:
            msg = QToolButton(self)
            msg.setText(text)
            msg.setProperty("type", type)
            msg.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            msg.setStyleSheet("* { border: none } ")
            if type == 0:
                msg.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxCritical))
                self.contentLayout.insertWidget(0, msg)
            else:
                msg.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxWarning))
                self.contentLayout.addWidget(msg)
            self.messages[msg] = wt
            self.updateCounters()
            
    def removeMsg(self, wt, text = None):
        for key, value in self.messages.items():
            if value == wt and (key.text() == text or not text):
                self.messages.pop(key)
                key.deleteLater()
        self.updateCounters()
            
    def updateCounters(self):
        errors, warnings = 0, 0
        for key in self.messages.keys():
            if key.property("type") == 0:
                errors += 1
            elif key.property("type") == 1:
                warnings += 1
                
        self.errorsCounter.setText("errors: {}".format(errors))
        self.warningsCounter.setText("warnings: {}".format(warnings))

        self.errorsFound.emit(errors > 0)