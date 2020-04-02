import os
import re
import sip
import json
import time
import maya.cmds as cmds
from shutil import copyfile
from Library import Camera, Scene
from collections import OrderedDict
import visibleReferences

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from maya import OpenMayaUI as omui

class ProgressDialog(QDialog):
    def __init__(self, parent = None):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi()

    def setStep(self, text):
        self.step.setText(text)
        
    def setScene(self, text):
        self.scene.setText(text)
        
    def setRange(self, min, max):
        self.progressBar.setRange(min, max)
        
    def setValue(self, value):
        self.progressBar.setValue(value)
        
    def value(self):
        return self.progressBar.value()
        
    def addMissingProps(self, items):
        self.propsList.addItems(items)
        
    def addNormalChars(self, items):
        self.charsList.addItems(items)
        
    def setupUi(self):
        self.setStyleSheet('* QLabel{ font-weight: bold; }')
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 3, 5, 3)
        self.setLayout(self.mainLayout)
        
        self.step = QLabel(self)
        self.step.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.step)
        
        self.scene = QLabel(self)
        self.scene.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.scene)
        
        self.progressBar = QProgressBar(self)
        self.mainLayout.addWidget(self.progressBar)
        
        separator = QFrame(self)
        separator.setFrameShape(QFrame.HLine)
        self.mainLayout.addWidget(separator)
        
        self.propsList = CollapsableList(u'Not founded props:', self)
        self.mainLayout.addWidget(self.propsList)
        
        self.charsList = CollapsableList(u'Chars without middle version:', self)
        self.mainLayout.addWidget(self.charsList)
        
        self.mainLayout.addSpacerItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding))
        
class CollapsableList(QWidget):
    def __init__(self, name, parent = None):
        super(CollapsableList, self).__init__(parent)
        self.setupUi()
        self.title.setText(name)
        
    def setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)
        
        self.titleLayout = QHBoxLayout(self)
        self.titleLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addLayout(self.titleLayout)
        
        self.expandButton = QToolButton(self)
        self.expandButton.setChecked(False)
        self.expandButton.setCheckable(True)
        self.expandButton.setFixedSize(15, 15)
        self.expandButton.setArrowType(Qt.RightArrow)
        self.expandButton.setStyleSheet('QToolButton { border: none }')
        self.expandButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.expandButton.toggled.connect(self.expandButtonClicked)
        self.titleLayout.addWidget(self.expandButton)
        
        self.title = QLabel(self)
        self.titleLayout.addWidget(self.title)
        
        self.counter = QLabel('0', self)
        self.titleLayout.addWidget(self.counter, 0, Qt.AlignRight)
        
        self.list = QListWidget(self)
        self.list.hide()
        self.mainLayout.addWidget(self.list)
        
    def expandButtonClicked(self, on):
        self.expandButton.setArrowType(Qt.DownArrow if on else Qt.RightArrow)
        self.list.setVisible(on)
        
    def addItems(self, items):
        self.list.addItems(items)
        self.counter.setText(str(self.list.count()))

def animationTemplate():
    #get episode and project dir path of scene
    ep, prjPath = getSceneInfo()
    if not ep or not prjPath:
        return False
    
    #select episode sets for animation template
    epSets = selectEpSets(prjPath, ep)
    if not epSets:
        QMessageBox.critical(None, 'Animation Template Error', u'Sets are not specified')
        return False
    
    #create progress dialog
    mayaWindow = omui.MQtUtil.mainWindow() 
    mayaWindow = sip.wrapinstance(long(mayaWindow), QWidget)
    progress = ProgressDialog(mayaWindow)
    progress.setWindowTitle('Animation Template')
    progress.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    progress.show()

    camAssets = processAnimatic(prjPath, ep, progress)
    if not camAssets:
        QMessageBox.critical(None, 'Animation Template Error', u'Unable to process animatic')
        return False
    
    missingRefs = set()
    if not createTemplate(prjPath, ep, camAssets, epSets, missingRefs, progress):
        QMessageBox.critical(None, 'Animation Template Error', u'Failed to create template')
        return False
    progress.addMissingProps(missingRefs)

    normalChars = set()
    if not createAnimationTemplate(prjPath, ep, camAssets, normalChars, progress):
        QMessageBox.critical(None, 'Animation Template Error', u'Failed to create animation template')
        return False
    progress.addNormalChars(normalChars)
    
    return True
    
def getSceneInfo():
    ep, prjPath = None, None
    
    sceneName = os.path.basename(cmds.file(sceneName=True, q=True))
    regexp = re.search('ep\d+', sceneName)
    if regexp:
        ep = regexp.group(0)
        if Scene.Scene.GetProject():
            prjPath = '{}/{}'.format(Scene.Scene.GetProject()[0], Scene.Scene.GetProjectName())
        else:
            QMessageBox.critical(None, 'Animation Template Error', u'Unable to get project path')
    else:
        QMessageBox.critical(None, 'Animation Template Error', u'Unable to get episode number of current scene')
    
    return ep, prjPath
    
def selectEpSets(prjPath, ep):
    #setsDirpath = 'D:/PythonScripts/TZ/ep107Set/maya'
    setsDirpath = '{}/assets/sets/{}Set/maya'.format(prjPath, ep)
    if not os.path.exists(setsDirpath):
        QMessageBox.critical(None, 'Animation Template Error', u"Directory '{}' doesn't exist".format(setsDirpath))
        return False
    
    setsFilepaths = []
    for filename in os.listdir(setsDirpath):
        if os.path.splitext(filename)[-1] == '.mb':
            setsFilepaths.append(setsDirpath + '/' + filename)
            
    if not setsFilepaths:
        QMessageBox.critical(None, 'Animation Template Error', u"No sets in directory '{}'".format(setsDirpath))
        return None
            
    mayaWindow = omui.MQtUtil.mainWindow() 
    mayaWindow = sip.wrapinstance(long(mayaWindow), QWidget)
    
    setsDialog = QDialog(mayaWindow)
    setsDialog.setWindowTitle('Animation Template')
    setsDialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
    
    setsLayout = QVBoxLayout(setsDialog)
    setsDialog.setLayout(setsLayout)
    
    setsLabel = QLabel(u'Select unnecessary sets for animation template', setsDialog)
    setsLabel.setAlignment(Qt.AlignCenter)
    setsLabel.setStyleSheet(' * { font-weight: bold; }')
    setsLayout.addWidget(setsLabel)
    setsLayout.addSpacing(10)
    
    setBoxes = []
    for filepath in setsFilepaths:
        setBox = QCheckBox(filepath.split('/')[-1], setsDialog)
        setBox.setProperty('filepath', filepath)
        setsLayout.addWidget(setBox)
        setBoxes.append(setBox)
    setsLayout.addSpacing(10)
        
    acceptButton = QPushButton('Ok', setsDialog)
    acceptButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
    acceptButton.clicked.connect(setsDialog.accept)
    setsLayout.addWidget(acceptButton, 0, Qt.AlignCenter)
    
    epSets = []
    if setsDialog.exec_():
        for setBox in setBoxes:
            if setBox.isChecked():
                epSets.append(setBox.property('filepath'))
    
    return epSets
        
def processAnimatic(prjPath, ep, progress):
    progress.setStep(u'Processing animatic [1/3]')
    
    animCameraDirpath = '{}/animatik/{}/cameras'.format(prjPath, ep)
    if not os.path.exists(animCameraDirpath):
        os.makedirs(animCameraDirpath)
    
    shots = cmds.sequenceManager(listShots=True)
    progress.setRange(1, 3 * len(shots))
 
    camAssets, camNames = [], []
    for sh in shots:
        progress.setScene(sh)
        qApp.processEvents()
        
        camName = cmds.shot(sh, currentCamera=True, q=True)
        startFrame = int(cmds.shot(sh, startTime=True, q=True))
        endFrame = int(cmds.shot(sh, endTime=True, q=True))
        endFrame = startFrame
        camNames.append(camName)
        
        regexp = re.search('^shot(.+)$', sh)
        if regexp:
            scene = '{}sc{}'.format(ep, regexp.group(1))
            camFile = '{}/animatik/{}/cameras/{}_mono.ma'.format(prjPath, ep, scene)
        else:
            QMessageBox.critical(None, 'Animation Template Error', u'Unable to get scene number {}'.format(sh))
            continue
            
        #export camera
        lightCameraDirpath = '{}/scenes/{}/{}/light'.format(prjPath, ep, scene)
        if not os.path.exists(lightCameraDirpath):
            os.makedirs(lightCameraDirpath)
        lightCameraScene = '{}/{}_mono.ma'.format(lightCameraDirpath, scene)
            
        cmds.select(camName, replace=True)
        cmds.camera(camName, lockTransform=True, e=True)
        cmds.setAttr('{}.s'.format(camName), lock=True)
        tmp = cmds.duplicate(camName)
        cmds.parent(tmp, world=True)
        cmds.rename(tmp, scene)
        cmds.file(rename=camFile)
        cmds.file(exportSelected=True, type='mayaAscii', force=True)
        cmds.delete('|' + scene)

        try:
            copyfile(camFile, lightCameraScene)
        except:
            QMessageBox.critical(None, 'Animation Template Error', u'Unable to copy file {} to {}'.format(camFile, lightCameraScene))
            return None
        
        meshs = {}
        chars, props, locations = [], [], []
        refs, meshs = visibleReferences.visibleReferences(camName, range(startFrame, endFrame + 1))
        for ref, visible in refs.items():
            if visible:
                filepath = cmds.referenceQuery(ref, filename=True)
                if '/assets/chars/' in filepath:
                    chars.append( {'name': ref, 'filepath': filepath} )
                elif '/assets/props/' in filepath:
                    props.append( {'name': ref, 'filepath': filepath} )
                elif '/assets/sets/' in filepath:
                    locations.append( {'name': ref, 'filepath': filepath} )
        
        if not chars and not props and not locations:
            QMessageBox.information(None, 'Animation Template Information', u"There is nothing in shot '{}'".format(camName))
            progress.setValue(progress.value() + 1) 
            continue
            
        for char in chars:
            char['transform'] = getTransform(char['name'])
            
        for prop in props:
            prop['transform'] = getTransform(prop['name'])
            prop['inTmplate'] = False
            
        camAssets.append( {'cam': {'name': camName, 'scene': scene, 'startFrame': startFrame, 'endFrame': endFrame, 'filepath': camFile}, 'chars': chars, 'props': props, 'sets': locations, 'meshs': meshs} )
        
        progress.setValue(progress.value() + 1)
        qApp.processEvents()
        
    '''
    jsonDirpath = '{}/animatik/{}/data'.format(prjPath, ep)
    if not os.path.exists(jsonDirpath):
        os.makedirs(jsonDirpath)
    jsonFilepath = jsonDirpath + '/ref_pos.json'
    with open(jsonFilepath, 'w') as outfile:
        json.dump(camAssets, outfile)
    '''
    
    #export all cameras
    camNames.sort()
    firstScene = re.search('sc(.+?)(v\d+|$)', camNames[0])
    lastScene = re.search('sc(.+?)(v\d+|$)', camNames[-1])
    if firstScene and lastScene:
        cmds.select(camNames, replace=True)
        cmds.file(rename='{0}/animatik/{1}/cameras/{1}sc{2}to{3}_mono.ma'.format(prjPath, ep, firstScene.group(1), lastScene.group(1)))
        cmds.file(exportSelected=True, type='mayaAscii', force=True)
    else:
        QMessageBox.critical(None, 'Animation Template Error', u'Unable to get first and last scene numbers')
        return None
    
    return camAssets

def getTransform(ref):
    transform = []
    
    nodeTypeValue = cmds.nodeType(ref)
    if nodeTypeValue == 'reference':
        if cmds.referenceQuery(ref, parentNamespace=True)[0]:
            return None

        refNamespace = cmds.referenceQuery(ref, namespace=True)
        if not refNamespace:
            print 'Unable to get namespace of reference {}'.format(item['name'])
            return None

        generalCT = cmds.ls('{}:general_CT'.format(refNamespace))
        if not generalCT:
            print 'Unable to find general controller of reference {}'.format(refNamespace)
            return None

        transform = {'translation': cmds.xform(generalCT, ws=True, t=True, q=True), 'rotation': cmds.xform(generalCT, ws=True, ro=True, q=True), 'scale': cmds.xform(generalCT, worldSpace=True, s=True, q=True)}
    else:
        print 'Unsupported node type {}'.format(nodeTypeValue)
        return None;

    return transform
    
def setTransform(ref, transform):
    nodeTypeValue = cmds.nodeType(ref)
    if nodeTypeValue == 'reference':
        refNamespace = cmds.referenceQuery(ref, namespace=True)
        if not refNamespace:
            print 'Unable to get namespace of reference {}'.format(item['name'])
            return None
            
        generalCT = cmds.ls('{}:general_CT'.format(refNamespace))
        if not generalCT:
            print 'Unable to find general controller of reference {}'.format(refNamespace)
            return None
            
        cmds.xform(generalCT, worldSpace=True, translation=(transform['translation'][0], transform['translation'][1], transform['translation'][2]))
        cmds.xform(generalCT, worldSpace=True, rotation=(transform['rotation'][0], transform['rotation'][1], transform['rotation'][2]))
        cmds.xform(generalCT, worldSpace=True, scale=(transform['scale'][0], transform['scale'][1], transform['scale'][2]))    
    else:
        print 'Unsupported node type {}'.format(nodeTypeValue)
        return None;
        
def createTemplate(prjPath, ep, camAssets, epSets, missingRefs, progress):
    progress.setStep(u'Creating template [2/3]')
    
    cmds.file(newFile=True, force=True)
    for epSet in epSets:
        cmds.file(epSet, i=True, preserveReferences=True, force=True)
    
    for camAsset in camAssets:
        progress.setScene(camAsset['cam']['scene'])
        qApp.processEvents()
        
        loadedRefs, visibleRefs, refsToUnload = set(), set(), set()
        for ref in cmds.ls(references=True):
            if cmds.referenceQuery(ref, isLoaded=True):
                loadedRefs.add(ref)
                for asset in camAsset['sets'] + camAsset['props']:
                    if asset['name'] == ref:
                        asset['inTmplate'] = True
        
        for asset in camAsset['sets'] + camAsset['props']:
            visibleRefs.add(asset['name'])
        
        if not cmds.objExists('hidden_layer_t'):
            cmds.select(clear=True)
            cmds.createDisplayLayer(name='hidden_layer_t', noRecurse=True)
        for mesh, visible in camAsset['meshs'].items():
            if not visible and cmds.objExists(mesh):
                cmds.editDisplayLayerMembers('hidden_layer_t', mesh, noRecurse=True)
        cmds.setAttr('hidden_layer_t.visibility', False)
        
        refsToUnload = loadedRefs.difference(visibleRefs)
        for ref in refsToUnload:
            try:
                cmds.file(unloadReference=ref)
            except:
                pass
        
        tmplateDirpath = '{}/scenes/{}/{}/tmplate'.format(prjPath, ep, camAsset['cam']['scene'])
        if not os.path.exists(tmplateDirpath):
            os.makedirs(tmplateDirpath)
        tmplateFilepath = '{}/{}_v{}_tmplate.mb'.format(tmplateDirpath, camAsset['cam']['scene'], fileVersion(tmplateDirpath))
        cmds.file(rename=tmplateFilepath)
        cmds.file(save=True, force=True, type='mayaBinary')
        camAsset['tmplate'] = tmplateFilepath
        
        for ref in refsToUnload:
            try:
                cmds.file(loadReference=ref)
            except:
                missingRefs.add(ref)
                
        cmds.delete('hidden_layer_t')
                
        progress.setValue(progress.value() + 1)
        qApp.processEvents()
    
    return True
    
def fileVersion(path):
    ver = 0
    for filename in os.listdir(path):
        regexp = re.search('_v(\d+)_', filename)
        if regexp:
            tmp = int(regexp.group(1))
            if (tmp > ver):
                ver = tmp
    ver = ver + 1
    return '{:03}'.format(ver)
    
def createAnimationTemplate(prjPath, ep, camAssets, normalChars, progress):
    progress.setStep(u'Creating animation template [3/3]')
    
    for camAsset in camAssets:
        progress.setScene(camAsset['cam']['scene'])
        qApp.processEvents()
        
        cmds.file(newFile=True, force=True)
        cmds.group(empty=True, name='chars_grp')
        cmds.group(empty=True, name='props_grp')
        cmds.group(empty=True, name='cameras_grp')
        
        tmplateNamespace = camAsset['tmplate'].split('.')[0].split('/')[-1]
        cmds.file(camAsset['tmplate'], reference=True, namespace=tmplateNamespace)
        cmds.playbackOptions(minTime=camAsset['cam']['startFrame'], maxTime=camAsset['cam']['endFrame'], animationStartTime=camAsset['cam']['startFrame'], animationEndTime=camAsset['cam']['endFrame'])
        
        cmds.file(camAsset['cam']['filepath'], i=True)
        cmds.parent(camAsset['cam']['scene'], 'cameras_grp')
        for cam in cmds.listCameras():
            cmds.setAttr(cam + '.renderable', cam == camAsset['cam']['scene'])
        
        for char in camAsset['chars']:
            middleCharFilepath = os.path.splitext(char['filepath'])[0] + '_middle.mb'
            if os.path.exists(middleCharFilepath):
                charFilepath = middleCharFilepath
            else:
                charFilepath = char['filepath']
                normalChars.add(char['name'])
                
            Scene.Scene.Reference(charFilepath)
            if char['transform']:
                setTransform(char['name'], char['transform'])
            cmds.parent(cmds.referenceQuery(char['name'], namespace=True) + ':root', 'chars_grp')
            
        for prop in camAsset['props']:
            if not prop['inTmplate']:
                Scene.Scene.Reference(prop['filepath'])
                setTransform(prop['name'], prop['transform'])
                parentNamespace = cmds.referenceQuery(prop['name'], parentNamespace=True)
                if parentNamespace:
                    if not parentNamespace[0]:
                        cmds.parent(cmds.referenceQuery(prop['name'], namespace=True) + ':root', 'props_grp')
            else:
                parentNamespace = cmds.referenceQuery(tmplateNamespace + ':' + prop['name'], parentNamespace=True)
                if parentNamespace:
                    if parentNamespace[0] == tmplateNamespace:
                        cmds.parent(cmds.referenceQuery(tmplateNamespace + ':' + prop['name'], namespace=True) + ':root', 'props_grp')
            '''
            if prop['transform']:
                Scene.Scene.Reference(prop['filepath'])
                setTransform(prop['name'], prop['transform'])
                cmds.parent(cmds.referenceQuery(prop['name'], namespace=True) + ':root', 'props_grp')
            if not cmds.objExists(prop['name']):
                Scene.Scene.Reference(prop['filepath'])
                if prop['transform']:
                    setTransform(prop['name'], prop['transform'])
            '''
            
        cmds.setAttr('defaultResolution.width', 2048)
        cmds.setAttr('defaultResolution.height', 858)
        cmds.setAttr('defaultResolution.pixelAspect', 1)
        cmds.setAttr('defaultResolution.deviceAspectRatio', 2.387)
        cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mayaSoftware', type='string')
            
        anmTmplateDirpath = '{}/scenes/{}/{}/anm/work'.format(prjPath, ep, camAsset['cam']['scene'])
        if not os.path.exists(anmTmplateDirpath):
            os.makedirs(anmTmplateDirpath)
        anmTmplateFilepath = '{}/{}_v{}_anm.ma'.format(anmTmplateDirpath, camAsset['cam']['scene'], fileVersion(anmTmplateDirpath))
        cmds.file(rename=anmTmplateFilepath)
        cmds.file(save=True, force=True, type='mayaAscii')
        
        progress.setValue(progress.value() + 1)
        qApp.processEvents()
        
    return True
    
if __name__ == '__main__':
    animationTemplate()