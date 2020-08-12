''' Copy Paste to maya
import sys
sys.path.append("FOLDER_TO_thisFILE")
import mapy;reload(mapy)
reload(mapy)
mapy.mapy_initUI()



proc do_close (string $arg) {
	deleteUI -window $arg;
}

HOTKEY :
F5 to_window for_refreshings:
import pymel.core as pm
pm.nameCommand ('hotkeyTest', ann='hotkey_test' , c = 'print "fafafafaf"' ) #with python Assign Command to mel
pm.hotkey(keyShortcut='F4', ctrlModifier=True,name='hotkeyTest')


to do:

Open Module last open info VVV
basename creation.ma XXX
save Module _rsg_Trees_kustA_kustB_TravaA  _c_ XXXX
click on tree inctance(example) check _toTRSV_ set selected transform for bake template transform layers XXXXX

!!!!! need Transformation Layers For All !!!!!!
big data

!!!!  test_save  _ANIM_ _CHAR_ _Dyn_ _RENDER_ a version r version in all scenes 
rewrite for using 
behavior for _CHAR_ version  only r 
and other _ROOT_ version  a r 

need loader RENDER ANIM VERSION


make instances to bbox persp query dist 150 all in this orig 
work with : marker _LOD_ make name to set bound box 

for land or floor  _s_ locatoros not to render
geo with name _s_ with scatter need generate poins normal apply if need
use for props auto find y positions and fix this
_toS_ this transform work with _s_ data to snap y positions


#IMPORT AOVS From Scene AND Base Render Setup For KD OCCL SPEC normals Diff Normals
import maya.cmds as cmds;import maya.mel as mel
nds = cmds.ls()
rsnodes = 0
rsstr = ''
for i in nds:
	if 'redshiftOptions' in i or 'defaultRedshiftPostEffects' in i or 'rsEnvironment' in i or 'rsPhysical' in i or 'rsVolumeScattering' in i or 'rsBokeh' in i or 'rsLensDistortion' in i or 'rsLensDistortion' in i or 'rsArea' in i or 'rsPortal' in i or 'rsIES' in i or 'rsDome' in i or 'sunDirection' in i or 'rsAov' in i or 'AO_mat' in i or 'DIFF_mat' in i or 'SPEC_mat' in i:
		cmds.delete(i)
cmds.file('//cacheServer/Project/lib/HOU/mapyPipe/ma_scenes/aovs_export.ma', i=True)
cmds.setAttr("redshiftOptions.imageFormat", 1)
#cmds.setAttr("redshiftOptions.preRenderMel", 'python(\"import arnoldToRIS;reload(arnoldToRIS);arnoldToRIS.loadMissingReferenceInstances()\");')
cmds.setAttr("defaultRenderGlobals.animation", 1)
cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 0)
cmds.setAttr("defaultResolution.width", 2048)
cmds.setAttr("defaultResolution.height", 858)
cmds.setAttr("defaultResolution.deviceAspectRatio", 2.387)
cmds.setAttr("defaultResolution.pixelAspect", 1)
cmds.setAttr("defaultRenderGlobals.enableDefaultLight", 0)
cmds.setAttr('redshiftOptions.preRenderMel' , """python("import arnoldToRIS;reload(arnoldToRIS);arnoldToRIS.loadMissingReferenceInstances()");""",type='string')
fs = cmds.playbackOptions(query=True, min=True)
fe = cmds.playbackOptions(query=True, max=True)
cmds.setAttr("defaultRenderGlobals.startFrame", fs)
cmds.setAttr("defaultRenderGlobals.endFrame", fe)



import os
import sys
sys.path.append("/cacheServer/Project/lib/HOU/mapyPipe")
import mapy;reload(mapy)
#-------------------------------------------------------
pathtoreffolders = mapy.findDynAndApply()
pathtoref_weight_ma = '//dataServer/Project/MALYSH/assets/chars/test/we.ma'
cmds.file(pathtoref_weight_ma, r=True)
g= os.listdir(pathtoreffolders)
for ref_folder in g:
	directory = pathtoreffolders + '/' + ref_folder
	lastabc = mapy.getlastFile(directory,endfile='.abc')
	abcfile =  directory + '/' + lastabc
	# get last file abc
	alembicNode = mel.eval('AbcImport -mode import "'+abcfile+'";')
	print alembicNode

geoFromAlembic = cmds.listConnections(u'botanikRN_v001_AlembicNode',s=False)
print geoFromAlembic


	#import abc 
	
	#reference weight
	
	#find geo apply blandshapes
	
	

MOTIONBLUR rs
setAttr "redshiftOptions.motionBlurFrameDuration" 0.665;
setAttr "redshiftOptions.motionBlurShutterEfficiency" 0.051;


#NUM EDITS in ref
import maya.cmds as cmds;import maya.mel as mel 
refs = mel.eval('ls -type reference')
num = 0
allnum = 0
for r in refs:
	try:
		ed = cmds.referenceQuery(r,editStrings=True)
	except:
		print r, 'pass'
	if ed != []:
		for e in ed:
			num += 1
			allnum += 1
	if num != 0:
		print r, num
	num = 0
print allnum


'''



import maya.cmds as cmds; import maya.mel as mel
import maya.OpenMayaUI as OpenMayaUI
import os,datetime,time,getpass
import random
import subprocess
from shutil import copyfile
from sys import platform as _platform

from shiboken2 import wrapInstance

from PySide2.QtWidgets import QApplication, QWidget ,QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QInputDialog
from PySide2.QtGui import QIcon, QFont, QPainter, QPixmap, QCursor
from PySide2.QtCore import Qt, QPoint


def colors_button(r):
	r *= 255
	rl = ((r + 5)*1.2)
	if rl >= 255:
		rl = 255
	rd = int(rl*0.7)
	return r,rl,rd

class myButton(QPushButton):
	def __init__(self, parent=None,d=False,c=False,t=False,*args, **kwargs):
		super(myButton, self).__init__(parent)
		self.setFont(QFont("Sanserif", 7))
		if d:
			self.clicked.connect(d)
			pass
		if c:
			r,rl,rd = colors_button(c[0])
			g,gl,gd = colors_button(c[1])
			b,bl,bd = colors_button(c[2])
			c1 = ' rgb('+str(r)+','+str(g)+','+str(b)+')'
			c2 = ' rgb('+str(rl)+','+str(gl)+','+str(bl)+')'
			c3 = ' rgb('+str(rd)+','+str(gd)+','+str(bd)+')'
			self.setStyleSheet("QPushButton{font-size: 14px;background-color:"+c1+"; color: black; border: black 2px} QPushButton:hover{background-color:"+c2+"; color: black; border: black 2px} QPushButton:pressed{background-color:"+c3+"; color: black; border: black 2px}")
		if t:
			self.setToolTip(str(t))


class mapyLayout(QWidget):
	def __init__(self,parent=None): #parentnone
		super(mapyLayout,self).__init__(parent=parent)
		self.setWindowTitle("Grid Layout")
		pos = QCursor.pos()
		self.setGeometry(pos.toTuple()[0],pos.toTuple()[1],0,0)
		#self.setIcon()
		self.refsLayout()
		self.animLayout()
		self.texmodLayout()
		self.rndLayout()
		self.lightLayout()
		self.dynLayout()
		vbox = QVBoxLayout()
		vbox.addWidget(self.groupBox)
		vbox.addWidget(self.groupBox2)
		vbox.addWidget(self.groupBox3)
		vbox.addWidget(self.groupBox4)
		vbox.addWidget(self.groupBox5)
		vbox.addWidget(self.groupBox6)
		self.setLayout(vbox)
		self.show()

	def setIcon(self):
		appIcon = QIcon("icon.png")
		self.setWindowIcon(appIcon)

	def refsLayout(self):
		self.groupBox = QGroupBox("Refs")
		self.groupBox.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("UnRef", lambda: unloadSelectedRefs(True), (0.2, 0.2, 0.3), 'unLoadSelected\nRef -> notes\n_UNLOADS_\nUnload Selected Reference;\nWrite Unloads to _UNLOADS_ node')
		gridLayout.addWidget(button, 0, 0)
		button2 = myButton("lctRef",lambda: LoadRef_FromClipboardText(), (0.2,0.2,0.3), 'LoadRef\nFrom\nClipboardText\nLoad refs from clipboard text')
		gridLayout.addWidget(button2, 1, 0)
		button21 = myButton("genCheck",lambda: PrintRefChecker(), (0.1,0.1,0.5), 'Print Check References Code Find Log (Only For Linux)')
		gridLayout.addWidget(button21, 2, 0)
		button3 = myButton("ulctRef",lambda: LoadRef_FromClipboardText(True), (0.2,0.2,0.3), 'unLoadRef\nFrom\nClipboardTextunLoad refs from clipboard text')
		gridLayout.addWidget(button3, 0, 1)
		button4 = myButton("pRef",lambda: printOPEN_REFS_COMMAND(), (0.2,0.2,0.3), 'Find Ref\nwork file\nprint\nprint to script editor command open reference')
		gridLayout.addWidget(button4, 1, 1)
		button5 = myButton("nsName",lambda: deleteNameSpacesFromSelected(), (0.5,0.4,0.7), 'rename selected node to without nameSpace')
		gridLayout.addWidget(button5, 2, 1)
		self.groupBox.setLayout(gridLayout)
	
	def animLayout(self):
		self.groupBox2 = QGroupBox("Anim")
		self.groupBox2.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("uptCuFLIP",lambda: flipbook(onlyCurrentFrame=True), (0.12,0.35,0.8), 'Update Current Frame in sequence of images')
		gridLayout.addWidget(button, 0,0)
		button1 = myButton("makeFLIP(1)",lambda: flipbook(samples=1), (0.15,0.55,0.95), 'Make Flipbook\nSlider or Selected\n(NOMB)\nMake Flipbook to sequence images with NoMotionBlur Samples')
		gridLayout.addWidget(button1, 1,0)
		button2 = myButton("makeFLIP(2)",lambda: flipbook(), (0.15,0.4,0.75), 'Make Flipbook to sequence images with 2 Samples MotionBlur')
		gridLayout.addWidget(button2, 2,0)
		button3 = myButton("makeFLIP(3)",lambda: flipbook(samples=3), (0.11,0.3,0.65), 'Make Flipbook to sequence images with 3 Samples MotionBlur')
		gridLayout.addWidget(button3, 0,1)
		button4 = myButton("openFLIP",lambda: TryOpenFlipbook(), (0.3,0.5,0.95), 'open Sequence Images(Flipbook) in mrViewer (check Folder Sound)')
		gridLayout.addWidget(button4, 1,1)
		self.groupBox2.setLayout(gridLayout)

	def texmodLayout(self):
		self.groupBox3 = QGroupBox("Tex/Mod")
		self.groupBox3.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("localFld",lambda: Make_Local_folder_From_Selected_Objects(), (0.9, 0.5, 0.2), 'MakeFolder\nlocalpath\nto clipboard\nLocal Folder For Selected object')
		gridLayout.addWidget(button, 0,0)
		button1 = myButton("expOBJ",lambda: ExportSelectedOBJs(), (0.5, 0.9, 0.2), 'Export sel\nto OBJs (folder\nto clipboard)\nexport Obj to local with preSmooth exported folder to Clipboard')
		gridLayout.addWidget(button1, 1,0)
		button5 = myButton("fileENV",lambda: setDATA_PROD_PATH(), (0.85, 0.75, 0.75), 'All File Nodes to DATA PROD PATH Environmet')
		gridLayout.addWidget(button5, 2,0)
		button2 = myButton("clipTexPath",lambda: getTexturePath_set_to_clipboard(), (0.5,0.9,0.2), 'textureServer\npath\nto clipboard\ncopy folder path to Clipboard')
		gridLayout.addWidget(button2, 0,1)
		button3 = myButton("clipTrans",lambda: CopyTransformToClipboard(), (0.65,0.46,0.86), 'Copy Selected\nTransform to\nclipboard as py Code\npaste py code  to python tab script')
		gridLayout.addWidget(button3, 1,1)
		self.groupBox3.setLayout(gridLayout)

	def rndLayout(self):
		self.groupBox4 = QGroupBox("Render")
		self.groupBox4.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("rndOutPath",lambda: SetLocalBatchImageOutfromClipboard(), (0.9, 0.2, 0.3), 'SetBatch\nImageOUT\nfrom scenePath\nsetup out image dir for local rendering from clipboard text path')
		gridLayout.addWidget(button, 0,0)
		button1 = myButton("BakeCams",lambda: selectedCamerasBakeToBatch(), (0.3, 0.6, 0.2), 'Bake Selected\nunParentCams\ntoBATCH_Cam\nfrom selected cameras bake one BAKE CAMERA use _fr0001_fr150 for set keyframes to bake')
		gridLayout.addWidget(button1, 1,0)
		button2 = myButton("LOW_RS",lambda: setIPR_Render(True), (0.3, 0.3, 0.7), 'LOW preset\nsss=0 subd=0\nMB=0 res=half)\nset ipr render with bruteforceGI and halfResolution')
		gridLayout.addWidget(button2, 2,0)
		button3 = myButton("HI_RS",lambda: setIPR_Render(False), (0.3, 0.3, 0.7), 'HI preset\nsss=1 subd=1\nMB=1 res=full)\nunset ipr render with Irradiance and fullResolution')
		gridLayout.addWidget(button3, 3,0)
		button4 = myButton("ExecMEL",lambda: executeMELnotes(), (0.3, 0.4, 0.1), ' from\nep../lightDATA/\npreRenderMels/*  execute mel Scripts for epizode')
		gridLayout.addWidget(button4, 4,0)
		button50 = myButton("NoteMat",lambda: reassigmMaterialFromNotes(), (0.8, 0.6, 0.3), 'Assign Lost Material to SelectedTransform from geo Notes \n select geo transform check notes if notes not empty Press This button')
		gridLayout.addWidget(button50, 5,0)
		button51 = myButton("txtNote",lambda: setTextNotesToSelectedTransfromsNodes(), (0.5, 0.3, 0.2), 'set text to Notes if selected shape/mesh note setuped to transform')
		gridLayout.addWidget(button51, 6,0)
		button9 = myButton("setACESdisp",lambda: setDisplayToACESRec709_disablePhotographicExposure(), (0.95,0.77,0.65), 'set Display to Aces and Disable Photographic Exposure')
		gridLayout.addWidget(button9, 0,1)
		button10 = myButton("RndSet",lambda: renderSetupAnimation(), (0.21,0.77,0.23), 'set Render Settings to current scene find camera Gi samples')
		gridLayout.addWidget(button10, 1,1)
		button5 = myButton("convTexAces",lambda: generate_rstexbin_aces(doConvert=True,bindAces=True), (0.95,0.35,0.45), 'Convert to ACES\ngenerate rstexbin\non cache server \n find Tiff files Copnvert to folder\nIF selected File nodes convert only selected!!!')
		gridLayout.addWidget(button5, 2,1)
		button6 = myButton("bindTexAces",lambda: generate_rstexbin_aces(doConvert=False,bindAces=True), (0.95,0.77,0.65), 'Dont Convert Aces\nOnly Bind\nto ConvertedACES')
		gridLayout.addWidget(button6, 3,1)
		button7 = myButton("bindTexTif",lambda: generate_rstexbin_aces(doConvert=False,bindAces=False), (0.95,0.77,0.65), 'Dont Convert Aces\nOnly Bind\nto TIFF')
		gridLayout.addWidget(button7, 4,1)
		button8 = myButton("rec1.8/sRGB",lambda: setFileNodesWithColorToRecGamma18(), (0.45,0.92,0.75), 'Toggle Color Files\ngamma1.8/sRGB\n Toggle all Color Files to gamma1.8 or sRGB colorspace')
		gridLayout.addWidget(button8, 5,1)

		self.groupBox4.setLayout(gridLayout)

	def lightLayout(self):
		self.groupBox5 = QGroupBox("Light")
		self.groupBox5.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("nkGradeLight",lambda: gradeNKtoSelectedLightsMaya_clipboard(), (0.7, 0.65, 0.2), 'light_color\nfrom nkGrade\n(clipboard)\n grade to clipboard from nuke and select light to setup color')
		gridLayout.addWidget(button, 0,0)
		button1 = myButton("setWhiteLight",lambda: gradeNKtoSelectedLightsMaya_clipboard(True), (0.7, 0.65, 0.2), 'Toggle\nLight Color\nto White\nset White and store color in notes')
		gridLayout.addWidget(button1, 1,0)
		button2 = myButton("genBatch",lambda: generateBatchRenderCodeToClipboard(), (0.85,0.85,0.33), 'Gen PyCode\nperLights perCams\nBatchRender\nFor selected Lights and Cams generate Code for Batch Redshift Render for per Light and perCams( _fr11_fr13 - single frames; _st01_en04 - range 01-04)')
		gridLayout.addWidget(button2, 2,0)
		button3 = myButton("attrPyCo",lambda: GenPyAttribValues(), (0.4, 0.35, 0.5), 'pyCode\nAttribs\nto Clipboard\nselected nodes store attrib values as py code')
		gridLayout.addWidget(button3, 0,1)
		button4 = myButton("attrPyCo(key)",lambda: GenPyAttribValues(onlyKeyable=True), (0.4, 0.35, 0.5), 'pyCode\nAttribs(keyable)\nto Clipboard\nselected nodes store attrib values(only keyable) as py code')
		gridLayout.addWidget(button4, 1,1)

		self.groupBox5.setLayout(gridLayout)

	def dynLayout(self):
		self.groupBox6 = QGroupBox("Cloth")
		self.groupBox6.setFont(QFont("Sanserif", 6))
		gridLayout = QGridLayout()
		gridLayout.setSpacing(2)
		gridLayout.setContentsMargins(2, 2, 2, 2)
		button = myButton("dynRef",lambda: findDynVersionREF(), (0.369571, 0.31, 0.202), 'Find Dyn\nVersion\nfor Selected\nFind Dyn Version For First Selected Character')
		gridLayout.addWidget(button, 0,0)
		button = myButton("selDynNodes",lambda: select_dyn_nodes_types(), (0.369571, 0.31, 0.802), 'select all dynamic nodes with types: fluidEmitter pointEmitter rigidBody hairSystem nRigid fluidShape nParticle nucleus particle nCloth rigidConstraint')
		gridLayout.addWidget(button, 0,1)
		button1 = myButton("setDYNode",lambda: Setup_Dyn(), (0.3, 0.5, 0.2), 'Setup _DYN_\ncams (near/far)\nignoreHwShader\ncreate _DYN_ Empty Group With Extra Attr; setup all cameras to 1:5000 near:far; ignoreHwShader for ALL meshes')
		gridLayout.addWidget(button1, 1,0)
		button2 = myButton("rangePre",lambda: setRange(), (0.2, 0.4, 0.5), 'Preroll Range\n(to start)\nSetup Range With Preroll; Jump to start frame with Preroll')
		gridLayout.addWidget(button2, 2,0)
		button3 = myButton("rangeAnim",lambda: setRange(False), (0.2, 0.4, 0.5), 'Anim Range\n(to start)\nSetup Animation Range; Jump to start frame')
		gridLayout.addWidget(button3, 3,0)
		button4 = myButton("setNucsFr",lambda: allNucleus(), (0.3, 0.4, 0.2), 'ALL Nucleus\nPreroll Frame\nSetup All Nucleus Nodes to Start Frame with preroll from _DYN_ Extra Attrib')
		gridLayout.addWidget(button4, 1,1)
		button5 = myButton("mkNCache",lambda: makeNCache(), (0.6, 0.4, 0.2), 'Make nCache\n(Selected)\nSetup All Nucleus Nodes to Start Frame with preroll from _DYN_ Extra Attrib')
		gridLayout.addWidget(button5, 2,1)
		button6 = myButton("expDynABC",lambda: makeDynABC(), (0.7, 0.3, 0.1), 'Export Alembic\n(only Selected)\nclipboard_path\nExport To Alembic;Copy dir with abc to clipboard')
		gridLayout.addWidget(button6, 3,1)
		self.groupBox6.setLayout(gridLayout)

def mapy_initUI():
	mayaMainwindow_ptr = OpenMayaUI.MQtUtil.mainWindow()
	mayaMainwindow = wrapInstance(long(mayaMainwindow_ptr),QWidget)
	mw = mapyLayout(parent=mayaMainwindow)#need parent
	mw.setWindowTitle('MAPY -> MAPY UI')
	mw.setWindowFlags(Qt.Window)
	mw.show()


def setTextToClipboard(t): # Set to Clipboard Text in maya
	QApplication.clipboard().setText(t)
	return None

def getTextFromClipboard(): # get From Clipboard Text
	t =QApplication.clipboard().text()
	return t

def Lin_Win_and_sep(): #return 0 is linux return 1 is windows
	if _platform == "linux" or _platform == "linux2":
		return 0, '/'
	elif _platform == "darwin":
		return 2, '/'
	elif _platform == "win32" or _platform == "win64":
		return 1, '\\'

def getlastFile(directory,endfile='.ma'): # Find last file with extension
	search_dir = directory
	os.chdir(directory)
	files = filter(os.path.isfile, os.listdir(search_dir))
	files.sort(key=lambda x: os.path.getmtime(x))
	lastfile = ''
	l = len(endfile)
	for f in reversed(files):
		if f[-l:] == endfile:
			lastfile = f
			break
	print(lastfile)
	return lastfile

def input_dialog(text, title, message):  #text - windowTitle; title -info for User; message - read/write user sring
	text, ok = QInputDialog.getText(None, text, title, text=message)
	if ok:
		return text

def timeStamp(read=0): # generate time stamp 
	ts = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d%H%M%S')
	TS = str(ts[4:6])+' '+str(ts[2:4])+' 20'+str(ts[0:2])+' ' + str(ts[6:8]) +':'+ str(ts[8:10])
	if read == 1:
		return TS
	else:
		return ts

def createLastOpenComment(path,ts): # generate file with date in folder with ma file when OPEN
	if os.path.isdir(path):
		comment = '_0pened_'+ts
		l = os.listdir(path)
		for f in l:
			if '_0pened_' in f:
				os.remove(path+'/'+f)
		userPC = getpass.getuser()
		#os.mknod(path+'/'+comment+'_by_'+userPC)
		with open(path+'/'+comment+'m_by_'+userPC,'a'):
			os.utime(path+'/'+comment+'m_by_'+userPC,None)
		return None
 
def findPROJ(): # ret putenv "PROJ" "Path" Set Last_open
	print ('find_PROJ_from_ma_path')
	mafile = cmds.file(query=True, l=True)[0]
	madir = os.path.dirname(mafile)
	ts = timeStamp(1).replace(':','h').replace(' ','__')
	createLastOpenComment(madir,ts)
	ma_elem = mafile.split('/')
	parfolders = []
	mode = 1
	if 'PROJ' in mafile:
		print ('asset_file')
		for p in ma_elem:
			if not 'PROJ' in p:
				if mode == 1:
					parfolders.append(p)
			else:
				mode=0
				parfolders.append(p)
				pass

		PROJ = os.sep.join(parfolders)
		return PROJ
	else:
		print ('collect_or_animation file')
		pdir = os.path.dirname(mafile)
		ppdir = os.path.dirname(pdir)
		pdir_content = os.listdir(pdir)
		for l in pdir_content:
			if l == 'PROJ':
				return pdir+os.sep+l
		pdir_content = os.listdir(ppdir)
		for l in pdir_content:
			if l == 'PROJ':
				return ppdir+os.sep+l

def setProj(): # find PROJ and Setup to var
	pr = findPROJ()
	print ('Found:', pr)
	if pr == None:
		cmds.warning('PROJ Not Found in File Path Scene\nSave Correct Scene!!!!!!!')
		return None
	line4 = '''putenv "PROJ" "'''+pr+'''";\n'''
	line5 = '''getenv "PROJ";\n'''
	mel.eval(line4+line5
)
def ZeroTransformation(path): # set Transformation  attribs to Matrix ident()
	attrVsDefVal = {'sx':1,'sy':1,'sz':1,'rx':0,'ry':0,'rz':0,'tx':0,'ty':0,'tz':0}
	for attr in attrVsDefVal:
		cmds.setAttr(path+'.'+attr, attrVsDefVal[attr])

def put_PROJ_procedure_to_mafile(filepath): # Set include FindProject to ma file in mel
	line0 = '''//Maya ASCII 2017ff05 scene\n'''
	line1 = '''python ("import sys; sys.path.append('//cacheServer/Project/lib/HOU/mapyPipe')");\n'''
	line2 = '''python("import mapy");\n'''
	line3 = '''string $pr = python ("mapy.findPROJ()");\n'''
	line4 = '''putenv "PROJ" $pr;\n'''
	line5 = '''getenv "PROJ";\n'''
	line6 = '''putenv "HOME_PROD_PATH" "/home";\n''' #HOME PROD PATH ????
	prepend = line0+line1+line2+line3+line4+line5+line6
	#print prepend
	with open(filepath, "r+") as f: s = f.read(); f.seek(0); f.write(prepend + s)
	print ('PROJ procedure setuped')

def select_in_ROOT(mode='r',selection='_ROOT_'): #select_in_ROOT('a','ALL') Select invert for delete then undo
	cmds.select(None)
	tosel = []
	if selection == 'ALL':
		root_childs = cmds.listRelatives('*',type='transform',ad=True,fullPath=True)
	else:
		root_childs = cmds.listRelatives(selection,type='transform',ad=True,fullPath=True)
	if root_childs == None:
		return tosel
	for ch in root_childs:
		if mode == 'a':
			if '_S_' in ch or not '_AR_' in ch:
				tosel.append(ch)
		elif mode == 's':
			if '_S_' in ch:
				tosel.append(ch)
		elif mode == 'r':
			if '_NR_' in ch or '_S_' in ch:
				tosel.append(ch)
		elif mode == 't':
			if '_TRSV_' in ch:
				tosel.append(ch)
	cmds.select(tosel)
	return tosel

def makeBakup(filepath_to_bak): # make Bakup given file to folder ./backup
	os.umask(0000)
	userPC = getpass.getuser()
	name = os.path.basename(filepath_to_bak)
	dir = os.path.dirname(filepath_to_bak)
	bakupdir = dir + '/backup'
	ts = timeStamp()
	if not os.path.isdir(bakupdir):
		os.mkdir(bakupdir)
	bakuppath = bakupdir + '/' + ts[:6] +'_'+ ts[6:] + '_' + name + '_backup_' + userPC
	copyfile(filepath_to_bak,bakuppath)

def makeBakup_unloadRefs_exportRoot_or_saveScene(): # MEGO SAVE and Export Root 
	#------------------------------------------------------SAVE_BACKUP------------------------------------------
	os.umask(0000)
	ma_current_path = cmds.file(query=True, l=True)[0]
	makeBakup(ma_current_path)
	name = os.path.basename(ma_current_path)
	dir = os.path.dirname(ma_current_path)
	dirname = dir.split('/')[-1]
	#------------------------------------------------------SAVE_BACKUP------------------------------------------
	#------------------------------------------------------SAVE MODES ------------------------------------------
	
	if len(cmds.ls("_ROOT_",r=True)) or len(cmds.ls("_CHAR_",r=True)):
		r = '_ROOT_'
		if len(cmds.ls("_CHAR_",r=True)):
			r = '_CHAR_'
			print ('Char')
		
		#prefix = input_dialog("Query", "Prop Name Prefix\nExamples:\n r - Render Version\n v - OpenGL version for Viewport2.0(colors)\n m - Modeling Version (not shader)\n a - RenderArchive Version\n p - Proxy Version(For hi poly models)", "r")
		r_file = dir + '/'+ '_r_.ma'
		a_file = dir + '/'+ '_a_.ma'
		s_file = dir + '/'+ '_s_.ma'
		linfile = dir + '/_.ma'
		#Save Current file
		print ('Save')
		cmds.file(save=True, type='mayaAscii')
		#file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "++";
		#file -force -options "v=0;" -typ "mayaAscii" -es -ch false -con false -chn false "++"; #without_history
		if len(cmds.ls("_RENDER_",r=True)):
			print ('SAVE_RENDER_CHAR')
			anim_file = dir +'/_exportRENDER_'+ name
			melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "'+anim_file+'";'
			cmds.select(None)
			cmds.select('_RENDER_')
			mel.eval(melcommand)
			put_PROJ_procedure_to_mafile(ma_current_path)
			return None
		if len(cmds.ls("_ANIM_",r=True)):
			print ('SAVE_ANIM')
			anim_file = dir +'/_exportANIM_'+ name
			melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "'+anim_file+'";'
			cmds.select(None)
			cmds.select('_ANIM_')
			mel.eval(melcommand)
			put_PROJ_procedure_to_mafile(ma_current_path)
			return None
		melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch false -con false -chn false "'+r_file+'";'
		if r == '_CHAR_':
			print ('SAVE_CHAR')
			print (r)
			cmds.select(r)
			melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "'+r_file+'";'
			mel.eval(melcommand)
		else:
			print ('SAVE_ROOT')
			cmds.select(None)
			ss = select_in_ROOT('r')
			mel.eval('doDelete;')
			cmds.select(r)
			mel.eval(melcommand)
			cmds.undo()
			cmds.undo()
			cmds.undo()
		if r == '_ROOT_':
			ss = select_in_ROOT('a')
			mel.eval('doDelete;')
			cmds.select(r)
			melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "'+a_file+'";'
			mel.eval(melcommand)
			cmds.undo()
			cmds.undo()
			cmds.undo()
		if r == '_ROOT_':
			ss = select_in_ROOT('s')
			melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es -ch true -con true -chn true "'+s_file+'";'
			if ss != []:
				mel.eval(melcommand)
			else:
				print ('s marker not used passed export')
		print (dirname)
		lname = '_L_'+dirname
		if len(cmds.ls(lname,r=True)):
			cmds.select(lname)
		else:
			for t in cmds.ls(type='transform',r=True):
				if ':' not in t:
					if '_L_' in t:
						print ('first _L_ founded')
						print (t)
						mel.eval('rename |'+t+' "'+lname+'";')
						cmds.select(lname)
						break
		#cmds.setAttr('_LINK_.refFolder', "$PROJ/"+dirname+"/*")
		try:
			mel.eval('setAttr -type "string" '+ lname +'.refFolder "$PROJ/'+dirname+'/*";')
		except:
			#print ''
			mel.warning('!!!!!!RefLink Not Found in scene!!!!!!')
			pass
		melcommand = 'file -force -options "v=0;" -typ "mayaAscii" -es "'+linfile+'";'
		mel.eval(melcommand)
		put_PROJ_procedure_to_mafile(ma_current_path)
		print ('SAVED')

	else:
		print ('Standart Save with backup And ProjSetup')
		cmds.file(save=True, type='mayaAscii')
		print ('SAVED')
		cmds.error('not Project nodes GLOB/ROOT/ANIM ')
	#------------------------------------------------------SAVE MODES ------------------------------------------

def createEmptyLink(): # vipilit potom generate Link 
	mt = '''createNode transform -n "_L_";
	addAttr -ci true -sn "refFolder" -ln "refFolder" -nn "Reference Folder" -dt "string";
	addAttr -ci true -sn "enableLoad" -ln "enableLoad" -nn "enableLoad(REND)" -at "long";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0.5 0.80000001 0.80000001 ;
	setAttr ".dla" yes;
	setAttr -cb on ".refFolder" -type "string" "$PROJ/HOST01_C001/*";
	setAttr -k on ".enableLoad" 1;
createNode nurbsCurve -n "curveShape1" -p "_L_";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 2 0 no 3
		3 0 0.90000000000000002 1
		3
		0 0 0
		0.5 1.2 0
		1 1.2 0
		;
	'''
	mel.eval(mt)

def printListPlugins(): #-> to Other File nado dopolnit codom list unpluget and list nodes from plugins and clean
	g = cmds.pluginInfo(query=True, listPlugins=True)
	print ('LIST_PLUGINS')
	for p in g:
		print ('	   pl -> ',p)
	return None

def find_all_links_in_scene_make_selected(): # find links for Referencing
	print ('find_all_links_in_scene_make_selected()')
	cmds.select(None)
	ma_current_path = cmds.file(query=True, l=True)[0]
	dir = os.path.dirname(ma_current_path)
	prop_name = dir.split('/')[-1]
	tosel = []
	for d in cmds.ls(type="transform",long=True):
		if prop_name in d:
			pass
		else:
			if cmds.ls(d+'.refFolder') != []:
				tosel.append(d)
	cmds.select(tosel)

def deleteLinkRefsSelected_notCHAR_notANIM(force=False): #only _ROOT_ nodes Delete References 
	print ('deleteLinkRefsSelected_notCHAR_notANIM')
	selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		print (s)
		try:
			try:
				ref = cmds.referenceQuery(s,referenceNode=True)
			except:
				f = cmds.listRelatives(s,type='transform',children=True,fullPath=True)
				ref = cmds.referenceQuery(f,referenceNode=True)
		except:
			continue
		if '_ROOT_' in s:
			print ('Delete Reference',ref)
			mel.eval('file -removeReference -referenceNode '+ ref)
		else:
			if force:
				mel.eval('file -removeReference -referenceNode '+ ref)
				print ('Delete forced All Refs; edits on _CHAR_ and _ANIM_ refs potracheno')
			else:
				print ('This CHAR or ANIM use manual delete in OUTLINER',ref)

def Delete_All_REFS_and_Load_selected_Links_ApplyData2(version='_r_',ALL=True,LOAD=True): # load references 
	print ('------LoadLinks:\n')
	mel.eval('refresh -suspend 1;')
	count = 0
	l = []
	if ALL:
		#select world links 
		find_all_links_in_scene_make_selected()
		selected = cmds.ls(sl=True, long=True) or []
	else:
		selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		f = cmds.listRelatives(s,type='transform',children=True,fullPath=True)
		if f != None:
			l += f
	ss =  l + selected
	cmds.select(l)
	deleteLinkRefsSelected_notCHAR_notANIM()
	proj = mel.eval('getenv "PROJ";')
	for s in ss:
		print ('\n---Load REF:')
		print (s,'\n')
		try:
			rf = cmds.getAttr(s[1:]+'.refFolder')
			count += 1
		except:
			rf = False #not attribute
		if rf:
			print ('Enable Load')
			#enableload = cmds.getAttr(s[1:]+'.enableLoad')
			assetname = rf.split('/')[1]
			#ns = rf.split('/')[1][:-4]
			ns = rf.split('/')[1]+'_'
			mafile = ''
			mafile = '$PROJ/<NAME_REF>/*'.replace('$PROJ',proj).replace('*',version).replace('<NAME_REF>',assetname) + '.ma'
			print (mafile)
			#len(cmds.ls(s + "|_g_",r=True)):
			if os.path.isfile(mafile):
				mel.eval('file -r -type "mayaAscii"  -ignoreVersion -gl -mergeNamespacesOnClash false -namespace "'+ns+'" -options "v=0;" "'+mafile+'";')
			else:
				print ('Not _a_ file for this link', s , 'skiped')
				continue
			err_name_space = ns + 'RN1'
			err = 0
			refname = ns + ':_ROOT_'
			refname2 = ns + ':_CHAR_'
			r_or_c = 0
			print (refname,refname2)
			try:
				try: mel.eval('parent '+refname+' '+s+';')
				except:
					mel.eval('parent '+refname2+' '+s+';')
					r_or_c = 1
			except:
				print ('not unique refs deleted on load', s)
				print (err_name_space)
				mel.eval('file -removeReference -referenceNode '+ err_name_space)
				err = 1
				count -= 1
			if not err:
				if r_or_c == 0:
					ZeroTransformation(s+'|'+refname)
				else:
					ZeroTransformation(s+'|'+refname2)
			continue

	mel.eval('refresh -suspend 0;')
	print ('\n------reLoaded Link refs - ' + str(count))
'''
def setToNotes(path,note='',get=0): # Set or Get from Notes abstract Text (rest position or resl light intenciti)
	if get == 0:
		if len(cmds.ls(path + ".notes",r=True)) == 0:
			mel.eval('addAttr -ci true -sn "nts" -ln "notes" -dt "string";')
		mel.eval('setAttr -type "string" '+ path +'.notes "'+ note +'";')
	else:
		r = cmds.getAttr(path +'.notes')
		return r
'''
def setToNotes(path,note='',get=0): # Set or Get from Notes abstract Text (rest position or resl light intenciti)
	if get == 0:
		if cmds.attributeQuery( 'notes', node=path,exists=True ) == False:
			cmds.select(None)
			cmds.select(path)
			mel.eval('addAttr -ci true -sn "nts" -ln "notes" -dt "string";')
		mel.eval('setAttr -type "string" '+ path +'.notes "'+ note +'";')
	else:
		r = cmds.getAttr(path +'.notes')
		return r

def setTextNotesToSelectedTransfromsNodes():
	cliptext = getTextFromClipboard()
	utext = input_dialog('to Selected Nodes', 'set this text', cliptext)
	selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		if cmds.objectType( s, isType='mesh'):
			s = cmds.listRelatives(s, parent=True, fullPath=True)[0]
		print(s,'notes',utext)
		setToNotes(s,utext,get=0)

def setREST_to_notes(path,set_clean=0): # set REST to Notes
	print ('setREST_to_notes')
	v = getTransformFromPath_PlusAttribList(path,['visibility'])
	if set_clean != 1:
		setToNotes(path,'_rest_'+str(v).replace('[','').replace(']','').replace(', ','_'))
	return v

def setMARKER(markerName='_TRSV_'): #markers -  _A_ _AR_ _NR_  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! NEED main field tag _tgTEG1_TEG2_TEG3tg_ 
	print ('setMARKER')
	sel = cmds.ls(sl=True, long=True) or []
	rest = 0
	newpath = ''
	for s in sel:
		if not markerName in s:
			if markerName == '_A_'or markerName == '_AR_' or markerName == '_NR_':
				pass
			newpath = s.split('|')[-1] + markerName
			nameto = newpath
			cmds.rename(s, nameto)
			rest = 1
		else:
			nameto =  s.split('|')[-1].replace(markerName,'')
			cmds.rename(s, nameto)
			rest = 0
		if markerName=='_TRSV_':
			if rest == 1: #SET rest transformation
				setREST_to_notes(newpath)
			else:
				setToNotes(newpath,'')

def fromChildTRSVSelect(): # selecte transform with TEG TRSV to manipulate
	print ('fromChildTRSVSelect()')
	selected = cmds.ls(sl=True, long=True) or []
	tosel = []
	for s in selected:
		pathtoTRSV = ''
		ss = s.split('|')
		fi = 0
		for p in ss[::-1]:
			if '_TRSV_' in p:
				fi = 1
			if fi == 1:
				pathtoTRSV = p + '|' + pathtoTRSV
		tosel.append(pathtoTRSV[:-1])
	if tosel == ['']:
		print ('Not use for Transformation')
		cmds.select(None)
		return None
	cmds.select(tosel)

def parse_line(line): # For floats and Bools : 'assemle -> |_ROOT_|group1|group21_TRSV_ -> 1.0_1.0_1.0_0.0_0.0_0.0_2.4_-0.1_-2.3_True\n'
	# For Rest Parce from Notes
	if line[:5] == '_rest':
		line = 'REST -> REST -> '+ line[5:] + '\n'
	ll = line[:-1].split(' -> ')
	ref = ll[0]
	path = ll[1]
	tr_v = ll[2].split('_')
	vals = []
	for t in tr_v:
		if t != '':
			v = None
			try:
				v = float(t)
			except:
				v = bool(t)
			vals.append(v)
	return ref,path,vals


def ApplyTransformationLine(currentFolder,line,links): # Apply Transformation from Line to TRSV transforms
	print ('ApplyTransformationLine()')
	ref,path,tr_v = parse_line(line)
	if ref == currentFolder: #this transform line to root
		print ('   to ROOT')
		setTransformFromPath_PlusAttribList(path,tr_v,['visibility'])
	else:
		print ('   to REF')
		ns = ref+'_'
		lp = path.split('|')
		s = '|'
		for el in lp:
			if el != '':
				s += ns +':'+ el + '|'
		pathwithns = s[:-1]
		print (pathwithns)
		for l in links:
			if ref in l:
				link_childs = cmds.listRelatives(l,ad=True,fullPath=True)
				for lc in link_childs:
					if pathwithns in lc:
						if lc[-6:] == '_TRSV_':
							setTransformFromPath_PlusAttribList(lc,tr_v,['visibility'])

def OverwriteTransformationLayer(mode=2):  # 1 - Overwrite Transformation	 2 - Apply Transformation	  3 - revert to REST
	print ('OverwriteOrApplyTransformatioLayerOrSetToREST()')

	ma_current_path = cmds.file(query=True, l=True)[0]
	dir = os.path.dirname(ma_current_path)
	propsname = os.path.basename(dir)

	if mode != 3:
		user_number,names = querySetNumber(where='/GLOBAL_TRANSFORM_LAYERS',title='GLOBAL_TRANSFORM_LAYERS:')
		
		if user_number == None:
			return None

		proj = mel.eval('getenv "PROJ";')
		tr_layers_folder = proj + '/GLOBAL_TRANSFORM_LAYERS'
		tr_file = names[int(user_number)-1]
		trpath =  tr_layers_folder+'/'+tr_file
		
		if mode==2: # Apply Transformation Layer
			transfrom_lines = []
			with open(trpath,'r') as f:
				transfrom_lines = f.readlines()
			find_all_links_in_scene_make_selected()
			links = cmds.ls(sl=True, long=True) or []
			for tl in transfrom_lines:
				ApplyTransformationLine(propsname,tl,links)
			cmds.select(None)
			return None
	else:
		print ('Revert to REST from notes')
		pass

	all = cmds.ls(type='transform',long=True) or []
	paths_data=[]
	for s in all:
		if '_TRSV_' in s:
			pathtoTRSV = ''
			ss = s.split('|')
			fi = 0
			for p in ss[::-1]:
				if '_TRSV_' in p:
					fi = 1
				if fi == 1:
					pathtoTRSV = p + '|' + pathtoTRSV
			if not pathtoTRSV[:-1] in paths_data:
				paths_data.append(pathtoTRSV[:-1])
	print ('---------------')
	lines = []
	for pd in paths_data:
		print (pd)
		if mode != 3:
			transforms_and_V = getTransformFromPath_PlusAttribList(pd,['visibility'])
			transforms_and_V = str(transforms_and_V).replace('[','').replace(']','').replace(', ','_')
			if '|_ROOT_' != pd[:7]:
				if ':' in pd: #this ref
					print ('Transformation layer from Rref')
					ns = pd.split('|')[-1].split(':')[0]
					refname = ns[:-1]
					ss = pd.split('|')
					path = ''
					for s in ss:
						if not '_L_'+ns[:-1] in s:
							path += '|'+s.replace(ns+':','')
					l = refname + ' -> ' + path[1:] + ' -> ' + transforms_and_V
					lines.append(l)
			else:
				#this root get proj name 
				if ':' in pd: #this root with namespaces need clean 
					print ('in Root nameSpaces : Clean name Spaces')
					continue
				else:
					path = pd
					print ('Transformation layer from Root')
					l = propsname + ' -> ' + path + ' -> ' + transforms_and_V
					lines.append(l)
		else:
			print ('	set to REST')
			v = setToNotes(pd,get=1)
			r,p,v = parse_line(v)
			setTransformFromPath_PlusAttribList(pd,v,['visibility'])

	#for kk in lines:
	#	print kk
	if mode == 1:
		makeBakup(trpath) # --------------------------------------DISABLE WRITE
		with open(trpath, 'w') as f:
			for i in lines:
				f.write(i + '\n')
	return None

	#Save with Backup file form query list Transformation layers

def querySetNumber(where='/GLOBAL_SELECTION_SETS',title='GlobalSelectionSets Names:',folder=0): # Global SETS from Folder transformations 
	proj = mel.eval('getenv "PROJ";')
	gssfolder = proj+where
	print (gssfolder)
	setsnames = os.listdir(gssfolder)
	i = 0
	text = ''
	names = []
	for sn in setsnames:
		add = 0
		if folder==0:
			if os.path.isfile(gssfolder+'/'+sn):
				add = 1
		else:
			if os.path.isdir(gssfolder+'/'+sn):
				add = 1
		if add != 0:
			i+=1
			names.append(sn)
			text+= str(i) + ' - ' + sn + '\n'
	user_number = input_dialog(title , text, 'number')
	try: 
		int(user_number)
	except:
		print ('Need integer set number !!!')
		return None,names
	return user_number,names

def unsetAllGlobalSelectionSets(): # not query find all_gs delete with key word   DELETE GLOBAL_SETs ALL  ??????
	pass

def setGloablSelectionSet(): #query folder for names And Setup To Selected TRSV nodes 
	#set name prefix gs_KROVAT_gs_podushka1 - where KROVAT name gloabl
	print ('setGloablSelectionSet')
	user_number,names = querySetNumber()
	if user_number:
		setshortname = names[int(user_number)-1].split(' - ')[0]
		setName = '_gs'+setshortname+'gs_'
		sel = cmds.ls(sl=True, long=True) or []
		for s in sel:
			if not setName in s:
				nameto =  setName + s.split('|')[-1]
				cmds.rename(s, nameto)
			else:
				nameto =  s.split('|')[-1].replace(setName,'')
				cmds.rename(s, nameto)

def selectWithGlobalSET(): #query folder for names and Select with name TRSV NODES 
	#select transforms with name gs_GLOBALSETNAME_gs*
	print ('selectWithGlobalSET')
	user_number,names = querySetNumber()
	if user_number == None:
		return None
	shortname = names[int(user_number)-1].split(' - ')[0]
	cmds.select(None)
	tosel = []
	for s in cmds.ls(type="transform",long=True):
		if '_TRSV_' in s:
			if '_gs'+shortname+'gs_' in s:
				tosel.append(s)
	cmds.select(tosel)

def toBoundSelected():
	print ('toBoundSelected')
	selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		if '_TRSV_' in s:
			cmds.setAttr(s+'.overrideEnabled' , 1)
			cmds.setAttr(s+'.overrideLevelOfDetail', 1)

def toUNBoundSelected():
	print ('toUNBoundSelected')
	selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		if '_TRSV_' in s:
			cmds.setAttr(s+'.overrideEnabled' , 0)
			cmds.setAttr(s+'.overrideLevelOfDetail', 0)

def drawBoundsToggleToSelectedLink():
	print ('drawBoundsToggle')
	selected = cmds.ls(sl=True, long=True) or []
	l = []
	for s in selected:
		l += cmds.listRelatives(s,ad=True,fullPath=True)
	ss =  l + selected
	for f in ss:
		if f[-3:] == '_g_':
			ld = cmds.getAttr(f+'.overrideLevelOfDetail')
			if ld == 0:
				#set to 1 ld oe
				cmds.setAttr(f+'.overrideEnabled' , 1)
				cmds.setAttr(f+'.overrideLevelOfDetail', 1)
			else:
				#set to 0 ld oe
				cmds.setAttr(f+'.overrideEnabled' , 0)
				cmds.setAttr(f+'.overrideLevelOfDetail', 0)
			print (f)

def getTransformFromPath_PlusAttribList(path,attrPlus=[]):
	attrVsDefVal = ['sx','sy','sz','rx','ry','rz','tx','ty','tz']
	val = []
	for attr in attrVsDefVal+attrPlus:
		v = cmds.getAttr(path+'.'+attr)
		val.append(v)
	return val

def setTransformFromPath_PlusAttribList(path,list_vals,attrPlus=[],makeKey=False):
	attrVsDefVal = ['sx','sy','sz','rx','ry','rz','tx','ty','tz']
	attrVsDefVal += attrPlus
	for attr,val in zip(attrVsDefVal,list_vals):
		cmds.setAttr(path+'.'+attr,val)
		if makeKey:
			cmds.setKeyframe(path+'.'+attr)

def selectedCamerasBakeToBatch():
	sel = cmds.ls(sl=True, long=True) or []
	camparms = []
	for s in sel:
		if '_fr' in s:
			splited = s.split('_fr')
			for frame in splited:
				try:
					frameint = int(frame)
				except: continue
				mel.eval('currentTime '+str(frameint) +' ;')
				f = getTransformFromPath_PlusAttribList(s,['focalLength','horizontalFilmAperture','verticalFilmAperture'])
				camparms.append(f)
		else:
			f = getTransformFromPath_PlusAttribList(s,['focalLength','horizontalFilmAperture','verticalFilmAperture'])
			camparms.append(f)
	tcam = cmds.camera()
	i = 0
	for c in camparms:
		i+=1
		mel.eval('currentTime '+str(i) +' ;')
		setTransformFromPath_PlusAttribList(tcam[0],c,['focalLength','horizontalFilmAperture','verticalFilmAperture'],True)
	cmds.rename(tcam[0],'BATCHCam')

def Setup_Dyn():
	fs = cmds.playbackOptions(query=True, min=True)
	fe = cmds.playbackOptions(query=True, max=True)
	
	print ('near and far camera setup')
	for d in cmds.ls(type="camera"):
		cmds.setAttr(d+".nearClipPlane",1)
		cmds.setAttr(d+".farClipPlane",5000)
	
	print ('ignoreHwShader is 1 for all mesh')
	for d in cmds.ls(type="mesh"):cmds.setAttr(d+".ignoreHwShader",1)

	cmds.select(None)
	if len(cmds.ls("|_DYN_",r=True)):
		print ('Dyn_Est')
	else:
		print ('Please setup _Dyn_ preroll')
		mel.eval("group -em -name _DYN_")
		mel.eval('addAttr -ln "anim_frame_start"  -at long  -dv '+str(int(fs)-1)+' |_DYN_;')
		mel.eval('setAttr -e-keyable true |_DYN_.anim_frame_start;')
		mel.eval('addAttr -ln "anim_frame_end"  -at long  -dv '+str(int(fe)+1)+' |_DYN_;')
		mel.eval('setAttr -e-keyable true |_DYN_.anim_frame_end;')
		mel.eval('addAttr -ln "preroll"  -at long  -dv 19 |_DYN_;')
		mel.eval('setAttr -e-keyable true |_DYN_.preroll;')
		print ('_Dyn_ NODE')

def setRange(set_preroll=True):
	if not len(cmds.ls("|_DYN_",r=True)):
		print ('Not_DYN_')
		return None
	FSTART = cmds.getAttr('|_DYN_.anim_frame_start')
	FEND = cmds.getAttr('|_DYN_.anim_frame_end')
	preroll = cmds.getAttr('|_DYN_.preroll')+1
	if set_preroll:
		PSTART = FSTART - preroll
	else:
		PSTART = FSTART
	mel.eval('currentTime '+str(PSTART)+' ;')
	mel.eval('playbackOptions -e -ast '+str(PSTART)+' -aet '+str(FEND)+';')
	mel.eval('playbackOptions -e -min '+str(PSTART)+' -max '+str(FEND)+';')

def allNucleus():
	if not len(cmds.ls("|_DYN_",r=True)):
		print ('Not_DYN_')
		return None
	FSTART = cmds.getAttr('|_DYN_.anim_frame_start')
	preroll = cmds.getAttr('|_DYN_.preroll')+1
	PSTART = FSTART - preroll
	for d in cmds.ls(type="nucleus"):
		print ('Setup Nucleos' , d)
		cmds.setAttr(d+".startFrame",PSTART)

def makeNCache():
	if not len(cmds.ls("|_DYN_",r=True)):
		print ('Not_DYN_')
		return None
	cf = mel.eval('currentTime -query;')
	setRange()
	mel.eval('refresh -suspend 1;')
	try:
		mel.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "","0","","0", "add", "0", "1", "1","0","1","mcx" } ;')
	except:
		pass
	mel.eval('refresh -suspend 0;')
	#setRange(False)
	mel.eval('currentTime '+str(cf)+' ;')

def recurciveFolderCreate(path):
	res = False
	osnum, sep = Lin_Win_and_sep()
	not_sep = '\\'
	if sep == not_sep:
		not_sep = '/'
	if sep not in path:
		path = path.replace(not_sep,sep)
	if osnum == 0:
		s = '//'
		for p in path.split(sep):
			if p != '':
				s+=p+'/'
				if not os.path.isdir(s):
					print ('Check_createion subFolder',s)
					os.mkdir(s)
					res = True
	else:
		if not os.path.isdir(path):
			os.makedirs(path)
			res = True
	return res

def findDynVersionREF(): # find FROM_SELECTED PERS DYN VERSION MENU SELECT VERSION
	print ('findDynVersionREF()')
	sel = cmds.ls(sl=True, long=True) or []
	if sel != []:
		ref = cmds.referenceQuery(sel[0],referenceNode=True)
		reff = cmds.referenceQuery(sel[0],filename=True)
		if not 'dyn' in reff:
			dynrf = '/work/dyn/'
		else:
			dynrf = '/'
		dynfolder = os.path.dirname(reff)+dynrf
		if os.path.isdir(dynfolder):
			items = os.listdir(dynfolder)
			mafiles = []
			for i in items:
				if '.ma' in i or '.mb' in i:
					mafiles.append(i)
			print (mafiles)
			text = ''
			i = 0
			for m in mafiles:
				text += str(i)+' - '+ m + '\n'
				i+=1
			us = input_dialog('refDynVersionNumber', text, '0')
			refVersionUser = mafiles[int(us)]
			path = dynfolder + refVersionUser
			mel.eval('file -loadReference "'+ref+'" -options "v=0" "'+path+'";')
		else:
			print ('not Found Dyn Dir: ' + dynfolder)
	else:
		print ('Select in Pers any children item')

def makeDynABC():
	if not len(cmds.ls("|_DYN_",r=True)):
		print ('Not_DYN_')
		return None

	fname = cmds.file(query=True, l=True)[0]
	print(fname,'fname')
	ffolder = os.path.dirname(fname).replace('/dyn/work','')
	print(ffolder,'ffolder')
	scname = os.path.basename(fname).split('.')[0]
	print(scname,'scname')
	abcdynname = ffolder + u'/cache/alembic/dyn/' + scname + u'.abc'
	#importfolder = '/'.join(fname.split('/')[:-3])
	#abcdynfolder = importfolder+'/cache/alembic/dyn'
	#try:
	#	abcdynfolder = '//dataServer/Project/'+abcdynfolder.split('/Project/')[1]
	#except:
	#	print ('In Saved File not Projet')
	#	pass
	abcfile_path = abcdynname
	userpath = input_dialog('Export ABC file', 'Set file Path (auto create Folders and copied to Clipboard) orig path is:\n'+ abcfile_path, abcfile_path)
	userdir = os.path.dirname(userpath)
	abcfile_path = userpath
	recurciveFolderCreate(userdir)
	abcpath = os.path.dirname(fname)
	lw, sep = Lin_Win_and_sep() #return 0 is linux return 1 is windows
	setTextToClipboard(userdir.replace('/',sep))
	print (abcpath , ' Copied to clipboard')
	FS = cmds.getAttr('|_DYN_.anim_frame_start')
	FE = cmds.getAttr('|_DYN_.anim_frame_end')
	selected = cmds.ls(sl=True, long=True) or []
	sel = ''
	for s in selected:
		sel += ' -root ' + s
	melcommand = 'AbcExport -j "-frameRange '+str(FS-1)+' '+str(FE+1)+' -uvWrite -worldSpace -eulerFilter -dataFormat ogawa '+sel+' -file '+abcfile_path+'";'
	mel.eval('refresh -suspend 1;')
	try:
		mel.eval(melcommand)
	except:
		pass
	mel.eval('refresh -suspend 0;')


def select_dyn_nodes_types():
	dyntypes = ['fluidEmitter','hairSystem','pointEmitter','rigidBody','nRigid','fluidShape','nParticle','nucleus','particle','nCloth','rigidConstraint']
	cmds.select(None)
	tosel = []
	for t in dyntypes:
		for d in cmds.ls(type=t):
			tosel.append(d)
	cmds.select(tosel)

def findDynAndApply():
	fname = cmds.file(query=True, l=True)[0]
	importfolder = '/'.join(fname.split('/')[:-3])
	abcdynfolder = importfolder+'/cache/alembic/dyn'
	return abcdynfolder

def ApplyDyn():	#-------------------------------------------------------

	sl = cmds.ls(sl=True)
	if len(sl) == 2:
		from_geo = sl[0]
		to_geo = sl[1]
		print (from_geo)
		print (to_geo)
		
		refs = mel.eval('ls -type reference')
		if 'weRN' in refs:
			print ('weimported')
		else:
			pathtoref_weight_ma = '//dataServer/Project/MALYSH/assets/chars/test/we.ma'
			cmds.file(pathtoref_weight_ma, r=True)
		wepa = cmds.ls('|we_chars_weight')
		ch = cmds.listRelatives(wepa)
		print (ch)
		weightpath = None
		for c in ch:
			print (c[3:-7], '---', to_geo)
			if c[3:-7] in to_geo:
				print ('weight',c)
				for cc in cmds.listRelatives(ch):
					if cc[3:] in to_geo:
						weightpath = c+'|'+cc
		print (weightpath)
			
		if weightpath != None:
			abcdynpath = from_geo
			splitgeo= abcdynpath.split(':')[-1]
			destpath = to_geo
			print (abcdynpath,weightpath,destpath)
			cmds.select(None)
			cmds.select(abcdynpath)
			cmds.select(weightpath,add=True)
			bl = cmds.blendShape(origin="world")
			print ('blendshape: ',bl)
			cmds.setAttr(bl[0]+'.'+splitgeo, 1)					
			
			weigths_str = setToNotes(weightpath,get=1)
			
			cmds.select(None)
			cmds.select(weightpath)
			cmds.select(destpath,add=True)
			bl_dest = cmds.blendShape(origin="world")
			cmds.setAttr(bl_dest[0]+'.we_'+splitgeo, 1)
			blendnode = bl_dest[0]
			i = 0
			for s in weigths_str.split('_'):
				sf = float(s)
				cmds.setAttr( blendnode +'.inputTarget[0].baseWeights['+str(i)+']', sf)
				i+=1
		else:
			print ('Weight not Found')

	else:
		print ('select From abc select Target')
		


def printOPEN_REFS_COMMAND():
	selected = cmds.ls(sl=True, long=True) or []

	if selected != []:
		print ('parce_sel')
	else:
		print ('not_selected')
		return None
	ref = cmds.referenceQuery(selected[0],referenceNode=True)
	print (ref)
	reffilepath = cmds.referenceQuery(ref,filename=True)	
	orig = reffilepath
	if not 'proxy' in reffilepath.lower():
		orig = reffilepath
	print (orig)
	dl = orig.split('/')[:-1]
	f = orig.split('/')[-1]
	wd = '/'.join(dl)+'/work'
	print (wd)
	wfildes = os.listdir(wd)
	os.chdir(wd)
	wfildes.sort(key=lambda x: os.path.getmtime(x))
	lw , sep = Lin_Win_and_sep()
	for f in wfildes:
		if os.path.isfile(wd+'/'+f):
			if lw == 0:
				print ('python /cacheServer/Project/lib/remoteExecution/lib/setup/maya/startMaya2017.py -rv 2644 '+wd+'/'+f)
			else:
				wrun = r'\\cacheServer\Project\lib\remoteExecution\lib\setup\maya\Python27\python.exe \\cacheServer\Project\lib\remoteExecution\lib\setup\maya\startMaya2017.py -rv 2644'
				print (wrun+' '+wd+'/'+f)
	if lw == 1:
		print (sep.join( wd.split('/') ))

def local_folder():
	o,s = Lin_Win_and_sep()
	startFolder = ''
	ts = timeStamp(1)[:-6].replace(' ', '_')
	time = timeStamp(1)[-6:].replace(' ', '_').replace(':','_')
	os.umask(0000)
	ma_current_path = cmds.file(query=True, l=True)[0]
	name = os.path.basename(ma_current_path).split('.')[0]
	new_folder = ts +'_'+ name + '_' + time
	if o == 0:
		print ('linux/mac')
		startFolder = os.getenv('HOME') + '/objexports/' + new_folder
	else:
		print ('win')
		startFolder = os.getenv('HOME') + '/objexports/' + new_folder
	return startFolder

def Make_Local_folder_From_Selected_Objects():
	print ('Make_Local_folder_From_Selected_Objects')
	o,s = Lin_Win_and_sep()
	
	startFolder = local_folder()
	#create dirs
	seppath = startFolder.split('/')
	pathappend = ''
	for f in seppath:
		pathappend += f + '/'
		if not os.path.isdir(pathappend):
			os.mkdir(pathappend)
	if o == 1:
		pathappend = s.join(pathappend.split('/'))
	print (pathappend , 'in Clipboard')
	setTextToClipboard(pathappend)

def ExportSelectedOBJs():
	print ('ExportSelectedOBJs')
	startFolder = local_folder()
	#create dir
	if os.path.isdir(startFolder):
		randint99 =  str(random.randrange(10,99))
		startFolder += '_'+randint99
	recurciveFolderCreate(startFolder)
	o,s = Lin_Win_and_sep()
	try:
		if o == 1:
			mel.eval('loadPlugin "C:/Program Files/Autodesk/maya2017/bin/plug-ins/objExport.mll";')
			setTextToClipboard('\\'.join(startFolder.split('/')))
		else:
			mel.eval('loadPlugin "/cacheServer/Project/lib/remoteExecution/usr/autodesk/maya2017Update4/bin/plug-ins/objExport.so";')
			setTextToClipboard(startFolder)
	except:
		print ('OBJExport plugin not enable')
	print (startFolder)
	text = '0 - Preserve Edges and Corners' + '\n' + '1 - Preserve Edges' + '\n' + '2 - No Smooting' + '\n' + '3 - Unparent (for instances without smooting)' + '\n' + '4 - Unparent (for instances with smooting)'
	us = input_dialog('Select Smooth UV Option', text, '0')
	print ('UserSelect:', us)
	s = cmds.ls(sl=True, long=True) or []
	p=0
	mel.eval('duplicate -rr;')
	print ('duplicat')
	if us == '3' or us == '4':
		for pw in range(10):
			try:
				mel.eval('parent -w;')
				p+=1
			except:pass
	#if len(s) > 1:
	#	mel.eval('polyUnite;')
	unite = False
	try:
		mel.eval('polyUnite;')
		print ('combine')
		unite = True
		p+=1
	except Exception as result:
		print (result)
	if us == '0' or us == '1' or us == '4':
		print ('polysmooth')
		if us == '0':
			#		 polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 1 -ofc 0 -ost 1 -ocr 0 -dv 2 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 komDet27_geo;
			mel.eval('polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 1 -ofc 0 -ost 1 -ocr 0 -dv 2 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1;')
		else:
			mel.eval('polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 2 -ofc 0 -ost 1 -ocr 0 -dv 2 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1;')
	else: 
		print ('!no_smooth!')
		pass
	template = '''file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" -typ "OBJexport" -es "<FOLDER>/<NAMEGEO>.obj";'''
	template = template.replace('<FOLDER>',startFolder)
	ss = s[0].replace('|','_')
	ss = ss.replace(':','')
	ss = ss[:50]
	com = template.replace('<NAMEGEO>',ss)
	print (com)
	mel.eval(com)
	print (p, ' - undo nums')
	print (us, ' - user choise')
	if us != '2':
		cmds.undo()
	if unite:
		cmds.undo()
	if us == '3' or us == '4':
		if p != 0:
			for undo_p in range(p-1):
				cmds.undo()
	cmds.undo()

def getTexturePath_set_to_clipboard():
	print ('getTexturePath_set_to_clipboard')
	o,s = Lin_Win_and_sep()
	ma_current_path = cmds.file(query=True, l=True)[0]
	dir = os.path.dirname(ma_current_path)
	if 'work/tex/' in dir or 'work/map/' in dir:
		pdir = os.path.dirname(dir)
		ppdir = os.path.dirname(pdir)
		dir = ppdir
	pdir = os.path.dirname(dir)
	ppdir = os.path.dirname(pdir)
	pathappend = ppdir+'/textures'
	if o == 1:
		pathappend = s.join(pathappend.split('/'))
	print (pathappend , 'in Clipboard')
	setTextToClipboard(pathappend)

def SetLocalBatchImageOutfromClipboard():
	print ('SetLocalBatchImageOutfromClipboard')
	#/dataserver/Project/MALYSH/scenes/ep101/master_light/work/images
	ma_current_path = cmds.file(query=True, l=True)[0]
	#print(ma_current_path)
	p = os.path.dirname(ma_current_path) + '/render'
	#p = getTextFromClipboard()
	o,s = Lin_Win_and_sep()
	if o == 1:
		p = '/'.join(p.split('\\'))
	print (p , ' - Batch output Images setuped....but not for Tracktor')
	tpm = '''workspace -fr "images" "<PATH>";'''
	mel.eval(tpm.replace('<PATH>',p))
	cmds.setAttr('defaultRenderGlobals.imageFilePrefix','seqName/img', type='string')

def gradeNKtoSelectedLightsMaya_clipboard(setWhite=False):
	print ('gradeNKtoSelectedLightsMaya_clipboard')
	if not setWhite:
		nk = getTextFromClipboard()
		if 'set cut_paste_input' in nk and 'white' in nk:
			afwhite = nk.split('white')[1]
			before_name = afwhite.split('name')[0]
			before_name = before_name.replace('{','').replace('}','')
			list = before_name.split(' ')
			try:
				rs = list[1]
				gs = list[2]
				bs = list[3]
			except:
				rs = list[1]
				gs = list[1]
				bs = list[1]
		else:
			print ('need Use in Nuke One grade node and one parm gain And Copy node to Clipboard')
			return None
	else:
		rs,gs,bs = '1','1','1'
		
	selected = cmds.ls(sl=True, long=True) or []
	tpl = '''setAttr "<NAME>.color" -type double3 <RS> <GS> <BS> ;'''
	for s in selected:
		if len(cmds.ls(s + ".notes",r=True)) == 0:
			mel.eval('addAttr -ci true -sn "nts" -ln "notes" -dt "string";')
		r = cmds.getAttr(s+'.color')
		if str(r[0][0]) == '1.0' and  str(r[0][1]) == '1.0' and  str(r[0][2]) == '1.0' : # IS WHITE
			n = cmds.getAttr(s+'.notes')
			rs = n.split(' ')[1]
			gs = n.split(' ')[2]
			bs = n.split(' ')[3]

		if setWhite:
			storecolor = '_ ' + str(r[0][0]) + ' ' + str(r[0][1]) +' '+ str(r[0][2])
			mel.eval('setAttr -type "string" '+ s +'.notes "'+ storecolor +'";')

		tplname = tpl.replace('<NAME>',s)
		tplcolor = tplname.replace('<RS>',rs).replace('<GS>',gs).replace('<BS>',bs)
		mel.eval(tplcolor)

def unloadSelectedRefs(redo=False):
	print ('unloadSelectedRefs')
	selected = cmds.ls(sl=True, long=True) or []
	
	cmds.select(None)
	
	if len(cmds.ls("|_UNLOADS_",r=True)):
		print ('_unload_')
	else:
		print ('Created ref Unload Node Do not Delete this')
		mel.eval("group -em -name _UNLOADS_")
		print ('_UNLOAD_ NODE')

	unloads = ''	
	for s in selected:
		ref = cmds.referenceQuery(s,referenceNode=True)
		mel.eval('file -unloadReference "' + ref +'"')
		unloads += ref + '\\n'
	if len(cmds.ls("|_UNLOADS_.notes",r=True)) == 0:
		cmds.select('|_UNLOADS_')
		mel.eval('addAttr -ci true -sn "nts" -ln "notes" -dt "string";')
		mel.eval('setAttr -type "string" "_UNLOADS_.notes" " ";')
	last_unloads = cmds.getAttr('|_UNLOADS_.notes').replace('\n','_|_')
	print 
	if last_unloads == None:
		last_unloads = ''
	last_unloads += '\\n' + unloads
	print (last_unloads)
	mel.eval('setAttr -type "string" "|_UNLOADS_.notes" "'+ str(last_unloads).replace('_|_','\\n') +'";')
	cmds.select('|_UNLOADS_')

def LoadRef_FromClipboardText(unload=False):
	print ('LoadRef_FromClipboardText')
	if unload: print ('Unload Mode\n----:')
	else: print ('load Mode\n----:')
	refs = getTextFromClipboard()
	for ref in refs.split('\n'):
		if ref != '' and ref != '\\n':
			try:
				if unload:
					mel.eval('file -unloadReference "' + ref +'"')
				else:
					mel.eval('file -loadReference "' + ref +'"')
			except:
				print ('text_notes bad')
				pass
	print ('----')
	cmds.select('|_UNLOADS_')

def CopyTransformToClipboard():
	t = '''
#Generate Python for Apply Transform from:
#<MAYASCENE>
#<SELPATH>
#Use in ScriptEditor Paste Python; Select this Block; Ctrl+Enter
import maya.cmds as cmds
sel = cmds.ls(sl=True, long=True) or []
AV = {'sx':<SX>,'sy':<SY>,'sz':<SZ>,'rx':<RX>,'ry':<RY>,'rz':<RZ>,'tx':<TX>,'ty':<TY>,'tz':<TZ>}
for a in AV:
	if a[0] in 'trs': # t-TRANSLATE, r-ROTATION, s-SCALE  ('ts' - apply to traslate and scale)
		cmds.setAttr(sel[0]+'.'+a, AV[a])
#Send as text to Friends :)
'''
	fname = cmds.file(query=True, l=True)[0]
	sel = cmds.ls(sl=True, long=True) or []
	attrs = ['sx','sy','sz','rx','ry','rz','tx','ty','tz']
	for a in attrs:
		v = cmds.getAttr(sel[0]+'.'+a)
		t = t.replace('<'+str(a).upper()+'>',str(v))
		t = t.replace('<MAYASCENE>', fname)
		t = t.replace('<SELPATH>', sel[0])
	setTextToClipboard(t)

def GenPyAttribValues(onlyKeyable=False):
	t_main = 'import maya.cmds as cmds;sel = cmds.ls(sl=True) or []\n'
	t_sel = '''p = '<NAME_LAST>';cmds.select(None);s = filter(lambda x: p in x, sel);cmds.select(s)\n'''
	t_int_float = 'try: cmds.setAttr(".<parmname>", <d1>)\nexcept: print ".<parmname> passed"\n'
	#t_int_float = 'setAttr ".<parmname>" <d1> ;\n'
	t_double3 = 'try:cmds.setAttr(".<parmname>", <d1>, <d2>, <d3>)\nexcept: print ".<parmname> passed"\n'
	#t_double3 = 'setAttr ".<parmname>" -type double3 <d1> <d2> <d3> ;\n'
	t_double2 = 'try:cmds.setAttr(".<parmname>", <d1>, <d2>)\nexcept: print ".<parmname> passed"\n'
	#t_double2 = 'setAttr ".<parmname>" -type double2 <d1> <d2> ;\n'
	t_string = 'try:cmds.setAttr(".<parmname>", "<d1>", type="string")\nexcept: print ".<parmname> passed"\n'
	#t_string = 'setAttr -type "string" .<parmname> "<d1>";\n'

	melcode = ''
	melcode += t_main
	selected = cmds.ls(sl=True,long=True) or []
	if selected == []:
		print ('Not Selected')
		return None
	s = selected[0]
	for s in selected:
		ss = s
		if ':' in s:
			ss = s.split(':')[-1]
		if '|' in ss:
			ss = ss.split('|')[-1]
		melcode += t_sel.replace('<NAME_LAST>',ss)
		if onlyKeyable:
			la = cmds.listAttr(s, keyable=True)
		else:
			la = cmds.listAttr(s)
		#dict = {}
		if la != None:
			for a in la:
				try:
					v = cmds.getAttr(s+'.'+a)
				except:
					v = None
				if v != None:
					c = v.__class__()
					if c != '':
						if c == []:
							#this doubles 
							if len(v) == 2:
								#print a,v, 'double2'
								melcode += t_double2.replace('<parmname>',a).replace('<d1>', str(v[0])).replace('<d2>', str(v[1]))
							if len(v) == 3:
								#print a,v, 'double3'
								melcode += t_double3.replace('<parmname>',a).replace('<d1>', str(v[0])).replace('<d2>', str(v[1])).replace('<d3>', str(v[2]))
							pass
						elif str(c) == '0':
							#this int
							melcode += t_int_float.replace('<parmname>',a).replace('<d1>', str(v))
							#print a,v, 'int'
						elif str(c) == '0.0':
							#print a,v, 'float'
							melcode += t_int_float.replace('<parmname>',a).replace('<d1>', str(v))
						elif str(c) == 'False':
							#print a,v, 'bool'
							i = 0
							if v: i = 1
							melcode += t_int_float.replace('<parmname>',a).replace('<d1>', str(i))
					else:
						#this may be string
						if len(v) > 0:
							#print a,v, 'string'
							melcode += t_string.replace('<parmname>',a).replace('<d1>', str(v))
						else:
							pass #print a,v, 'NONN'
	setTextToClipboard(melcode)
	print (melcode)
	print ('long list attribs in Clipboard')

def get_scene_parms(mapath):
	print(mapath,' mapath')
	rpl = ''
	t = ''
	if 'anm' in mapath:
		rpl = mapath.replace('Project/','|||').replace('/scenes/','|||').replace('/anm/','|||')
		t = 'anm'
	elif 'dyn' in mapath:
		rpl = mapath.replace('Project/','|||').replace('/scenes/','|||').replace('/dyn/','|||')
		t = 'dyn'
	elif 'check' in mapath:
		rpl = mapath.replace('Project/','|||').replace('/scenes/','|||').replace('/check/','|||')
		t = 'check'
	elif 'light' in mapath:
		rpl = mapath.replace('Project/','|||').replace('/scenes/','|||').replace('/light/','|||')
		t = 'light'
	else:
		t = 'other'
	if rpl == '':
		return 'TEST', 'epTEST', 'scTEST','flipbook'
	split_repl = rpl.split('|||')
	#print split_repl
	print(split_repl,' split_rpl')
	try:
		PROJECT = split_repl[1]
	except:
		PROJECT = 'untitled'
	try: e_s = split_repl[2].split('/')
	except: e_s = ['None','None']
	sc = e_s[-1]
	try: srep = split_repl[2].replace('/'+sc,'')
	except: srep = 'None'
	#print PROJECT, srep, sc,t
	return PROJECT, srep, sc,t


def rename_Minus(folder_with_sequence):
	files = os.listdir(folder_with_sequence)
	sorted_files = sorted(files)
	last = sorted_files[-1]
	print (last,' last')
	lastnumber = 0
	for f in files:
		if '.ove' in f:
			laststr = f.split('_')[1]
			lastnumber = int(laststr)
	zerofile = ''
	files_to_rename = []
	MinusEnabled = False
	for f in sorted_files[::-1]:
		if not '.ove' in f:
			if '-' in f or '0000' in f:
				if '-' in f :
					lastnumber+=1
					MinusEnabled = True
					files_to_rename.append((f,lastnumber))
				if '0000' in f:
					zerofile = f
	files_to_rename.append((zerofile,lastnumber+1))
	if MinusEnabled:
		print ('Minus Enabled Renamenig ....')
		for f in files_to_rename:
			print (f)
			numfile = f[0].split('.')[-2]
			new_file_name = f[0].replace(numfile, (str(f[1])).zfill(4))
			print (new_file_name)
			newpath = folder_with_sequence+'/'+new_file_name
			if os.path.isfile(newpath):
				os.remove(newpath)
				pass
			os.rename(folder_with_sequence+'/'+f[0],newpath)
	return None

def join_pixmap(p1, p2, mode=QPainter.CompositionMode_SourceOver):
	s = p1.size()
	result =  QPixmap(s)
	result.fill(Qt.transparent)
	painter = QPainter(result)
	painter.drawPixmap(QPoint(), p1)
	painter.setOpacity(0.5)
	painter.setCompositionMode(mode)
	painter.drawPixmap(result.rect(), p2, p2.rect())
	painter.end()
	return result


def flipbook(onlyCurrentFrame=False, samples=2):
	print ('flipbook()')
	#print(__file__) #//cacheServer/Project/lib/HOU/mapyPipe/mapy.py
	#set cam
	selected = cmds.ls(sl=True,long=True) or []
	cmds.select(None)
	mayaFile = cmds.file (q=1, sn=1).split('/')[-1].split('.')[0]
	mayaFilePath = os.getenv('HOME') + '/flipbooks/' + mayaFile + '/'
	print(mayaFilePath,'mayaFilePath')

	if mayaFilePath == u'':
		print('untitled_scene')
		mayaFilePath = os.getenv('HOME') + '/flipbooks_untitled.ma'

	l = cmds.ls('|cameras_grp')
	findmode = False
	animationCamera = u'perspShape'
	if l == []:
		print ('custom camera')
		findmode = True
		cams = cmds.ls(type='camera')
		for c in cams:
			if not c in [u'frontShape', u'perspShape', u'sideShape', u'topShape']:
				if 'sr' in c and 'ep' in c and 'sc' in c:
					print (c,'Found')
					animationCamera = c
	if not findmode:
		animationCamera = cmds.listRelatives(l, allDescendents=True, type='camera')[0]
	print (animationCamera)

	aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
	timeRangeRed = cmds.timeControl(aTimeSlider, q=True, rangeArray=True)

	activedCamera = mel.eval('lookThru -q;')

	w = cmds.getAttr("defaultResolution.width")
	h = cmds.getAttr("defaultResolution.height")
	print (w, h , '-  From Render Resolution !!!!')


	cmds.lookThru(animationCamera, 'perspView')
	
	dres = cmds.getAttr('%s.displayResolution'% animationCamera)
	dgm = cmds.getAttr('%s.displayGateMask'% animationCamera)
	dgmo = cmds.getAttr('%s.displayGateMaskOpacity'% animationCamera)
	dgmc = cmds.getAttr('%s.displayGateMaskColor'% animationCamera)
	osca = cmds.getAttr('%s.overscan'% animationCamera)
	panz = cmds.getAttr('%s.panZoomEnabled'% animationCamera)

	#set_cam_attribs For Plablast
	cmds.setAttr('%s.displayResolution'% animationCamera, 1)
	cmds.setAttr('%s.displayGateMask'% animationCamera, 0.888)
	cmds.setAttr('%s.displayGateMaskOpacity'% animationCamera, 1)
	cmds.setAttr('%s.displayGateMaskColor'% animationCamera, 0.0, 0.0, 0.0, type='double3')
	cmds.setAttr('%s.overscan'% animationCamera, 1.1)
	cmds.setAttr('%s.panZoomEnabled'% animationCamera, 0)
	print ('setuped camera', animationCamera)

	modelPanelList = cmds.getPanel(typ='modelPanel')

	for eachModelPanel in modelPanelList:
		cmds.modelEditor (eachModelPanel, e=1, nurbsCurves=0) #+gpucache
		cmds.modelEditor (eachModelPanel, e=1, joints=0)
		cmds.modelEditor (eachModelPanel, e=1, locators=0)
		cmds.modelEditor (eachModelPanel, e=1, sel=0)
		
	print ('nurbs  hided')
		
	
	sceneparms = get_scene_parms(mayaFilePath)
	print(sceneparms)

	#collectshot deta
	projectName = sceneparms[0]
	shotName = sceneparms[2]
	time = datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M %p")
	userName = os.getenv('USERNAME')
	#........
	startTime = int(cmds.playbackOptions(q=1, ast=1))
	endTime = int(cmds.playbackOptions(q=1, aet=1))

	timeLabel = 'Frame [ %i - %i ]'% (startTime, endTime)

	currentFps = mel.eval('currentTimeUnitToFPS')

	#remove all headUpsDisplays
	headsUpDisplayList = cmds.headsUpDisplay(q=1, lh=1)
	if headsUpDisplayList:
		for eachHeadUpDisplay in headsUpDisplayList:
			cmds.headsUpDisplay (eachHeadUpDisplay,rem=1)
	#set my head up
	cmds.headsUpDisplay ('HUDProjectName', s=0, b=0, bs='large', lfs='large', l=projectName+' - '+shotName)
	cmds.headsUpDisplay ('HUDTime', s=4, b=0, bs='small', lfs='small', l=time)
	cmds.headsUpDisplay ('HUDUserName', s=5, b=0, bs='small', lfs='small', l=userName)
	cmds.headsUpDisplay ('HUDFrame', s=6, b=0, bs='small', lfs='small', l=timeLabel, c='int(round(cmds.currentTime (q=1)))', atr=1) # frames start end
	cmds.headsUpDisplay ('HUDMyLabel', s=7, b=0, bs='small', lfs='small', l=mayaFilePath+'    (press "K" to reload Seq..)')
	cmds.headsUpDisplay ('HUDFps', s=9, b=0, bs='small', lfs='small', l='fps - %f'% currentFps)

	#sceneparms = get_scene_parms(mayaFilePath)
	seqParms = path_to_flipbooks(mayaFilePath,sceneparms)
	seqPath = seqParms[0]
	createdNewFolder = seqParms[3]
	cmds.select (animationCamera)
	ct = cmds.currentTime(q=1)
	#currentPanel = cmds.getPanel(wf=1)
	timeRangeSel = [cmds.playbackOptions(q=1,min=True),cmds.playbackOptions(q=1,max=True)]

	rangeSlider_center = ''
	rangeSlider_begin = ''
	rangeSlider_ended = ''
	rangesInt = [0,0]
	offset = 0.133333
	
	first_last_frames = [startTime,endTime-1]
	if not createdNewFolder:
		first_last_frames = []
	
	if int(timeRangeRed[0]) == int(timeRangeRed[1])-1:
		print ('not Selected Update range Slider')
		rangesInt = [int(timeRangeSel[0]),int(timeRangeSel[1])]
		rangeSlider_center = '-startTime ' + str(int(timeRangeSel[0]))  +' -endTime '+ str(int(timeRangeSel[1]))
		rangeSlider_begin = '-startTime ' + str(timeRangeSel[0]-offset)  +' -endTime '+ str(timeRangeSel[1]-offset)
		rangeSlider_ended = '-startTime ' + str(timeRangeSel[0]+offset)  +' -endTime '+ str(timeRangeSel[1]+offset)
	else:
		print ('selected range')
		rangeSlider_center = '-startTime ' + str(int(timeRangeRed[0])) +' -endTime '+ str(int(timeRangeRed[1]))
		rangeSlider_begin = '-startTime ' + str(timeRangeRed[0]-offset)  +' -endTime '+ str(timeRangeRed[1]-offset)
		rangeSlider_ended = '-startTime ' + str(timeRangeRed[0]+offset)  +' -endTime '+ str(timeRangeRed[1]+offset)
		rangesInt = [int(timeRangeRed[0]),int(timeRangeRed[1])]
	if onlyCurrentFrame:
		rangeSlider_center = '-startTime ' + str(int(ct)) +' -endTime '+ str(int(ct))
		rangeSlider_begin = '-startTime ' + str(ct-offset)  +' -endTime '+ str(ct-offset)
		rangeSlider_ended = '-startTime ' + str(ct+offset)  +' -endTime '+ str(ct+offset)
		rangesInt = [int(ct),int(ct)]

	percent = 85
	frame_pre = seqPath+'_0'
	frame_post = seqPath+'_1'
	frame_center = seqPath+'_2'
	img_paths_list = []
	img_pathsB_list = []
	img_pathsE_list = []
	img_pathsC_list = []
	for fr in range(rangesInt[0],rangesInt[1]+1) + first_last_frames:
		img_source_pre = frame_pre+ '.'+str(fr).zfill(4)+'.jpg'
		img_source_post = frame_post+ '.'+str(fr).zfill(4)+'.jpg'
		img_source_center = frame_center+ '.'+str(fr).zfill(4)+'.jpg'
		img_out_mb =  seqPath+ '.' + str(fr-startTime+1).zfill(4) + '.jpg'
		img_paths_list.append(img_out_mb)
		img_pathsB_list.append(img_source_pre)
		img_pathsE_list.append(img_source_post)
		img_pathsC_list.append(img_source_center)


	if samples == 1:
		# BLOCK for 1 samples
		print(rangeSlider_center,'   - first_sampleRange')
		mel.eval('playblast '+rangeSlider_center+' -format image -filename "'+frame_center+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		
		print ('Start convert')
		for out,pre in zip(img_paths_list,img_pathsC_list):
			print (out , '  - flipframe')
			out_pic = QPixmap(pre)
			#picture2 = QtGui.QPixmap(post)
			#out_pic = join_pixmap(picture1, picture2)
			out_pic.save(out,"jpg")
			if os.path.isfile(pre):
				os.remove(pre) 
			print ('-------')

	if samples == 2:
		# BLOCK for 2 samples
		print(rangeSlider_begin,'   - first_sampleRange')
		mel.eval('playblast '+rangeSlider_begin+' -format image -filename "'+frame_pre+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		print(rangeSlider_ended,'   - last_sampleRange')
		mel.eval('playblast '+rangeSlider_ended+' -format image -filename "'+frame_post+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		
		if first_last_frames != []:
			pass
		print ('Start merge')
		for out,pre,post in zip(img_paths_list,img_pathsB_list,img_pathsE_list):
			print (out , '  - flipframe')
			picture1 = QPixmap(pre)
			picture2 = QPixmap(post)
			out_pic = join_pixmap(picture1, picture2)
			out_pic.save(out,"jpg")
			if os.path.isfile(pre):
				os.remove(pre) 
			if os.path.isfile(post):
				os.remove(post)
			print ('-------')


	if samples == 3:
		# BLOCK for 3 samples
		print(rangeSlider_center,'   - last_sampleRange')
		mel.eval('playblast '+rangeSlider_center+' -format image -filename "'+frame_center+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		print(rangeSlider_begin,'   - first_sampleRange')
		mel.eval('playblast '+rangeSlider_begin+' -format image -filename "'+frame_pre+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		print(rangeSlider_ended,'   - last_sampleRange')
		mel.eval('playblast '+rangeSlider_ended+' -format image -filename "'+frame_post+'" -sequenceTime 0 -clearCache 1 -viewer 0 -showOrnaments 1 -offScreen  -fp 4 -percent '+str(percent)+' -compression "jpg" -quality 10 -widthHeight '+str(w)+' '+str(h)+';')
		
		if first_last_frames != []:
			pass
		print ('Start merge')
		for out,pre,post,center in zip(img_paths_list,img_pathsB_list,img_pathsE_list,img_pathsC_list):
			print (center)
			print (pre)
			print (post)
			print (out , '  - flipframe')
			picture1 = QPixmap(pre)
			picture2 = QPixmap(post)
			picture3 = QPixmap(center)
			bl = join_pixmap(picture1, picture2)
			out_pic = join_pixmap(bl,picture3)
			out_pic.save(out,"jpg")
			if os.path.isfile(pre):
				os.remove(pre) 
			if os.path.isfile(post):
				os.remove(post)
			if os.path.isfile(center):
				os.remove(center)
			print ('-------')

	ct = cmds.currentTime(ct)
	headsUpDisplayList = cmds.headsUpDisplay(q=1,lh=1)
	for eachHeadUpDisplay in headsUpDisplayList:
		cmds.headsUpDisplay (eachHeadUpDisplay,rem=1)

	#revert Active Cam settings
	cmds.setAttr('%s.displayResolution'% animationCamera, dres)
	cmds.setAttr('%s.displayGateMask'% animationCamera, dgm)
	cmds.setAttr('%s.displayGateMaskOpacity'% animationCamera, dgmo)
	cmds.setAttr('%s.displayGateMaskColor'% animationCamera, dgmc[0][0],dgmc[0][1],dgmc[0][2], type='double3')
	cmds.setAttr('%s.overscan'% animationCamera, osca)
	cmds.setAttr('%s.panZoomEnabled'% animationCamera, panz)

	for eachModelPanel in modelPanelList:
		cmds.modelEditor (eachModelPanel, e=1, nurbsCurves=1)
		cmds.modelEditor (eachModelPanel, e=1, joints=1)
		cmds.modelEditor (eachModelPanel, e=1, locators=1)
		cmds.modelEditor (eachModelPanel, e=1, sel=1)
	cmds.select(selected)

	mel.eval('lookThru '+activedCamera+';')
	#OVEFILE
	folder = seqParms[1]
	jpgseq = seqParms[0] + u'.%4d.jpg'
	sound = seqParms[2]
	si = cmds.playbackOptions(q=1, ast=1)
	offset = 0
	if si <= 0:
		offset = si
		si = 1
	ei = cmds.playbackOptions(q=1, aet=1)
	ei = ei + offset
	s = str(1) 
	ns = str(int(si))
	e = str(int(ei))
	ss = ns.zfill(4)
	ee = e.zfill(4)
	out_mont = str(int(ei-si+1))
	seqspeed = str(currentFps/25.0)
	fps_i = str(int(currentFps))
	ove_file = folder + '/' + ss + '_' + ee + '_' + fps_i + '.ove'
	w = int(w*(percent*0.01))
	h = int(h*(percent*0.01))

	t = ''
	t += '<project>\n'
	t += '  <media>\n'
	t += '    <footage id="1" url="'+jpgseq+'" speed="'+seqspeed+'" startnumber="'+s+'" > </footage>\n'
	t += '    <footage id="2" url="'+sound+'" speed="1" startnumber="1"> </footage>\n'
	t += '  </media>\n'
	t += '  <sequences>\n'
	t += '    <sequence width="'+str(w)+'" height="'+str(h)+'" framerate="'+fps_i+'.0000000000" afreq="48000" open="1">\n'
	t += '      <clip enabled="1" clipin="0" in="0" out="'+out_mont+'" track="-1" media="1" stream="0"> </clip>\n'
	t += '      <clip enabled="1" clipin="0" in="0" out="'+out_mont+'" track="0" media="2" stream="0"> </clip>\n'
	t += '    </sequence>\n'
	t += '  </sequences>\n'
	t += '</project>\n'
	
	if os.path.isfile(ove_file):
		return None
	else:
		with open(ove_file, 'w') as f:
			f.write(t)

	#if not interupted:
	#	print 'succes Flipbook'
	#else:
	#	info = 'interupted Flipbook Use Update Current Frame To revert Layout'
	#	cmds.warning(info)
	#	print info
	#return None

def path_to_flipbooks(mayaFilePath,sceneparms):
	server_begin = os.path.dirname(mayaFilePath)
	#folder = server_begin + 'playblast/' + sceneparms[1] + '/flipbooks_'+sceneparms[3]+'/' + sceneparms[2]
	#folder = server_begin + '/flipbook/' + sceneparms[1] + '/flipbooks_'+sceneparms[3]+'/' + sceneparms[2]
	folder = server_begin + '/flipbook/'
	#sound = server_begin + 'sound3d/' + sceneparms[1] + '/' + sceneparms[2] + '.wav'
	sound = server_begin + '/sound/audio.wav'
	soundFolder = server_begin + '/sound/PASTE_HERE_audio.wav_file_for_flipbook'
	created = recurciveFolderCreate(folder)
	recurciveFolderCreate(soundFolder)
	return folder + '/' + sceneparms[2] , folder , sound , created
	
def openFlipbookFolder():
	mayaFilePath = cmds.file (q=1, sn=1)
	sceneparms = get_scene_parms(mayaFilePath)
	seqParms = path_to_flipbooks(mayaFilePath,sceneparms)
	folder = seqParms[1]
	print(folder)
	
def TryOpenFlipbook():
	#\\cacheserver\Project\lib\HOU\mapyPipe\programs\mrViewer-v5.3.1-Windows-64\bin\mrViewer.exe
	#Firse File .jpg
	# -a 
	# Wav file
	#mayaFilePath = cmds.file (q=1, sn=1)

	mayaFile = cmds.file (q=1, sn=1).split('/')[-1].split('.')[0]
	mayaFilePath = os.getenv('HOME') + '/flipbooks/' + mayaFile + '/'
	print(mayaFilePath,'mayaFilePath')

	if mayaFilePath == u'':
		print('untitled_scene')
		mayaFilePath = os.getenv('HOME') + '/flipbooks_untitled.ma'

	sceneparms = get_scene_parms(mayaFilePath)
	seqParms = path_to_flipbooks(mayaFilePath,sceneparms)
	folder = seqParms[1]
	sound = seqParms[2]
	nameShot = sceneparms[2]
	print(folder)
	#print(__file__) #//cacheServer/Project/lib/HOU/mapyPipe/mapy.py
	
	s = cmds.ls( type='audio')
	soundfile_in_maya = ''
	try:
		soundfile_in_maya = cmds.getAttr(s[0]+'.filename')
	except:pass
	if not os.path.isfile(sound):
		if soundfile_in_maya != '':
			if os.path.isfile(soundfile_in_maya):
				sound = soundfile_in_maya
	#print(__file__,'__file__') #('D:/wxBrowser/mapy\\mapy.pyc', '__file__')
	mapyPath = __file__.split('mapy\\')[0]
	mr53 = 'bin_portables/mrViewer-v5.3.1-Windows-64/bin/mrViewer.exe'
	#mrv = '//cacheserver/Project/lib/HOU/mapyPipe/programs/mrViewer-v5.3.1-Windows-64/bin/mrViewer.exe'
	mrv = mapyPath + '/' + mr53
	currentMR = ''
	if not os.path.isfile(mrv):
		if os.path.isdir('C:/Program Files'):
			for pr in os.listdir('C:/Program Files'):
				if 'mrViewer' in pr:
					currentMR = 'C:/Program Files/' + pr + '/bin/mrViewer.exe'
	if os.path.isfile(currentMR):
		mrv = currentMR
	if Lin_Win_and_sep()[0] == 0:
		print ('Linux Detected')
		mrv = 'mrViewer'
	if os.path.isdir(folder):
		jpg = folder + '/' + nameShot+ '.0000.jpg'
		snd = sound
		flag = '-a'
		if os.path.isfile(mrv):
			print ('launch Sub Process')
			subprocess.Popen([mrv,jpg,flag,snd])
		if Lin_Win_and_sep()[0] == 0:
			subprocess.Popen([mrv,jpg])
	pass
	
def TryOpenFlipbook_old_olivie():
	mayaFilePath = cmds.file (q=1, sn=1)
	sceneparms = get_scene_parms(mayaFilePath)
	seqParms = path_to_flipbooks(mayaFilePath,sceneparms)
	folder = seqParms[1]
	
	currentFps = mel.eval('currentTimeUnitToFPS')
	fps_i = str(int(currentFps))
	si = cmds.playbackOptions(q=1, ast=1)
	if si <= 0:
		si = 1
	ei = cmds.playbackOptions(q=1, aet=1)
	s = str(int(si))
	e = str(int(ei))
	ss = s.zfill(4)
	ee = e.zfill(4)

	ove_file = folder + '/' + ss + '_' + ee + '_' + fps_i + '.ove'
	print(ove_file)
	OlivieAppPath = '//server-ad/SYSVOL/mel.local/olive/olive-editor.exe'
	if Lin_Win_and_sep()[0] == 0:
		print ('Linux Detected')
		#cmds.error("   >> FlipBook for Windows !!!")
		OlivieAppPath = '/cacheserver/Project/lib/remoteExecution/olivie_montage/Olive.AppImage'
		os.system(OlivieAppPath + ' ' + ove_file)
		return None
	#OlivieAppPath = '/cacheserver/Project/lib/remoteExecution/olivie_montage/Olive.AppImage'
	#pathto_mr_viewer = '//cacheServer/Project/lib/HOU/mapyPipe/programs/mrViewer-v5.3.1-Windows-64/bin/mrViewer.exe'
	e=0
	if os.path.isfile(OlivieAppPath):
		if os.path.isfile(ove_file):
			subprocess.Popen([OlivieAppPath,ove_file])
		else: e=1
	else: e=1
	if e:
		cmds.error("   >> FlipBook not Found !!!")


def executeMELnotes(num=0):
	#_PRE_RENDER_MELNOTES_1
	import maya.cmds as cmds
	import maya.mel as mel
	mayaFilePath = cmds.file (q=1, sn=1)
	spl_mayaFilePath = mayaFilePath.split('/scenes/')
	path_toep =  spl_mayaFilePath[0] + '/scenes/'
	numep = spl_mayaFilePath[1].split('/')[0]
	fix_mel_path = path_toep+numep+'/lightDATA/preRenderMels'
	if os.path.isdir(fix_mel_path):
		#print 'open window with files'
		files = os.listdir(fix_mel_path)
		if files != []:
			print ('files')
			txt_files = 'Select file Numbers to Execute:\n'
			listfiles = []
			index = 0
			msg = ''
			for f in sorted(files):
				if '.mel' in f:
					print ('\n\nLaunch Mel :' + f)
					#input_dialog('MEL', 'Select file Numbers to Execute:\n0 - file.mel\n1 - file2.mel\n2 - file3.mel\n', '0 1 2')
					txt_files += str(index) + ' - ' + f + '\n'
					msg += str(index) + ' '
					listfiles.append(f)
					index +=1
				else:
					print ('\nnot mel file')
			
			umsg = input_dialog('MEL', txt_files, msg)
			if umsg != None:
				nums = umsg.split(' ')
				for n in nums:
					if n != '':
						try:
							file = listfiles[int(n)]
						except:
							print ('not a number in field !!!!')
							return None
						print ('\n\n - Launch MEL - ',file)
						with open(fix_mel_path+'/'+file) as w:
							co = w.readlines()
						for c in co:
							print ('command:',c)
							mel.eval(c)
					else:
						pass
			else:
				print ('canceled')
		else:
			print ('\nnot mel files in this dir', fix_mel_path)
	else:
		print (fix_mel_path,' Not Found Dir "preRenderMels" in lightDATA folder')
		return None

	#//dataServer/Project/MALYSH/scenes/ep23/ep23sc46/anm/work/ep23sc46_v189_anm.ma


	return None
	name = '_PRE_RENDER_MELNOTES_' + str(num)
	l = cmds.ls(type='transform')
	found = False
	for t in l:
		tname = t
		if ':' in t:
			nslost = t.split(':')[-1]
			tname = nslost
		if name == tname:
			print ('found' + t)
			if len(cmds.ls(t + ".notes",r=True)) != 0:
				#print 'i Found notes'
				n = cmds.getAttr(t + ".notes")
				found = True
				mel.eval(n)
				print ('Executed: ', n)
			else:
				print ('Not found Script Notes in ' + t)
				found = True
	if not found:
		print ('Not Found Template Nodes named _PRE_RENDER_MELNOTES_*')

def setIPR_Render2020(setHalf=False):
	renderlayers = cmds.ls(type="renderLayer")
	for layer in renderlayers:
		if not ':' in layer:
			try:
				cmds.editRenderLayerGlobals(crl=layer)
			except:pass
			w = cmds.getAttr("defaultResolution.width")
			h = cmds.getAttr("defaultResolution.height")
			setIPR = 0
			sss_tes_mb = 1
			if setHalf:
				if w > 1200:
					w /= 2
					h /= 2
					setIPR = 1
					sss_tes_mb = 0
			else:
				if w < 1200:
					w *= 2
					h *= 2
		cmds.setAttr("defaultResolution.width",w)
		cmds.setAttr("defaultResolution.height",h)
		cmds.setAttr("redshiftOptions.progressiveRenderingEnabled", setIPR)
		cmds.setAttr("redshiftOptions.progressiveRenderingNumPasses", 64)
		cmds.setAttr("redshiftOptions.subsurfaceScatteringEnable", sss_tes_mb)
		cmds.setAttr("redshiftOptions.tessellationDisplacementEnable", sss_tes_mb)
		cmds.setAttr("redshiftOptions.motionBlurEnable",sss_tes_mb)
	return None

def setIPR_Render(setHalf=False):
	w = cmds.getAttr("defaultResolution.width")
	h = cmds.getAttr("defaultResolution.height")
	setIPR = 0
	sss_tes_mb = 1
	if setHalf:
		if w > 1200:
			w /= 2
			h /= 2
			setIPR = 1
			sss_tes_mb = 0
	else:
		if w < 1200:
			w *= 2
			h *= 2
	cmds.setAttr("defaultResolution.width",w)
	cmds.setAttr("defaultResolution.height",h)
	cmds.setAttr("redshiftOptions.progressiveRenderingEnabled", setIPR)
	cmds.setAttr("redshiftOptions.progressiveRenderingNumPasses", 64)
	cmds.setAttr("redshiftOptions.subsurfaceScatteringEnable", sss_tes_mb)
	cmds.setAttr("redshiftOptions.tessellationDisplacementEnable", sss_tes_mb)
	cmds.setAttr("redshiftOptions.motionBlurEnable",sss_tes_mb)
	return None

def perLightRender(name='', cam='persp', frame=-999, lightEnb='', disableLights=[], dualGI=True):
	#cmds.rsRender(render=True, blocking=True, animation=True, cam='camera_1')
	pass

def generateBatchRenderCodeToClipboard():
	print('generateBatchRenderCodeToClipboard()')
	topTemplate = '''#-----Copyed Code for Launch Batch Render : 
#Check Out Dir:
renderOUT = '<PATH>'

import maya.cmds as cmds; import maya.mel as mel;import os
if not os.path.isdir(renderOUT):os.mkdir(renderOUT)
cmds.workspace(fileRule=['images',renderOUT])
setAttr "defaultRenderGlobals.enableDefaultLight" 0;
setAttr "redshiftOptions.aovGlobalEnableMode" 0;
def perLightRender(frame,name,cam,lightEnb,disableLights):
	cmds.setAttr('defaultRenderGlobals.animation',1);cmds.setAttr('defaultRenderGlobals.startFrame',frame);cmds.setAttr('defaultRenderGlobals.endFrame',frame)
	cmds.setAttr('defaultRenderGlobals.imageFilePrefix','perLightRender/'+name, type='string')
	for c in cmds.ls(type='camera'): cmds.setAttr(c+'.renderable',0);cmds.setAttr(cam+'.renderable',1)
	for l in disableLights:
		cmds.setAttr(l+'.visibility',0)
		cmds.setAttr(lightEnb+'.visibility',1)
		try:
			cmds.setAttr(lightEnb+'.colorR',1.00001)
			cmds.setAttr(lightEnb+'.colorG',1.00001)
			cmds.setAttr(lightEnb+'.colorB',1.00001)
		except:pass
	print('RENDER:',frame, name);cmds.rsRender(render=True, blocking=True, animation=True, cam=cam)
	print('----------------------------------------------------')
	
a = cmds.getAttr('defaultRenderGlobals.animation');s = cmds.getAttr('defaultRenderGlobals.startFrame');e = cmds.getAttr('defaultRenderGlobals.endFrame')
	'''
	mayaFilePath = cmds.file (q=1, sn=1)
	pf = '/'.join(mayaFilePath.split('/')[:-1])
	p = pf + '/BatchCamsLights_v01' 
	topTemplate = topTemplate.replace('<PATH>',p)
	currentFrame = cmds.currentTime(q=1)
	cameraDefault = '|persp'
	all = cmds.ls(long=True) or []
	sel = cmds.ls(sl=True,long=True) or []
	cams=[]
	lights=[]
	typeLights = ['volumeLight','areaLight','spotLight','pointLight','directionalLight','ambientLight','RedshiftDomeLight','RedshiftPhysicalLight','RedshiftIESLight','mesh']
	for a in all:
		if a in sel:
			if a != None:
				shape = cmds.listRelatives(a, shapes=True)
				if shape != None:
					t = cmds.objectType(shape[0])
					if t == 'camera':
						cams.append(a)
					if t in typeLights:
						lights.append(a)
	frame_cam = []
	if cams == []:
		cams = cameraDefault
	for c in cams:
		noneFr = False
		noneStEn = False
		if '_fr' in c:
			splited = c.split('_fr')
			for frame in splited:
				try:
					frameint = int(frame)
				except: continue
				frame_cam.append((c,frameint))
		else:
			noneFr = True
		if '_st' in c and '_en' in c:
			st_to_end = c.split('_st')[-1]
			st_end = st_to_end.split('_en')
			try:
				frame_st = int(st_end[0])
				frame_en = int(st_end[1])
			except: continue
			for f in range(frame_st,frame_en+1):
				frame_cam.append((c,f))
		else:
			noneStEn = True
		if noneFr and noneStEn:
			frame_cam.append((c,int(currentFrame)))
	if frame_cam == []:
		frame_cam.append((cameraDefault,currentFrame))
	to_copy = ''
	if lights == []:
		lights = ['',]
	for fc in frame_cam:
		for l in lights:
			name = fc[0].replace('|','')+'__'+l.replace('|','')
			#perLightRender(name, cam, frame, lightEnb, disableLights, dualGI=True)
			hidelights = ''
			enbLight = ''
			for ll in lights:
				if ll != l:
					hidelights += '"' + ll+'",'
				else:
					enbLight = 'lightEnb="'+ll+'"'
			disableLights = 'disableLights=['+hidelights[:-1]+']'
			to_copy += 'perLightRender(frame='+str(fc[1])+', name="'+name+'", cam="'+fc[0]+'", '+enbLight+', '+ disableLights + ')\n'
	withTop = topTemplate +'\n'+ to_copy
	withTail = withTop + '''\ncmds.setAttr('defaultRenderGlobals.animation',a);cmds.setAttr('defaultRenderGlobals.startFrame',s);cmds.setAttr('defaultRenderGlobals.endFrame',e)'''
	print (withTail)
	setTextToClipboard(withTail) # Set to Clipboard Text in maya
	#WHEN NONE LIGHT BUT SELECTED CAMS  ALL LIGHTS 
	#HEN NONE CAMs Persp main CAM
	#WHEN NONE FR ST  EN IN CAMS SET CURRENT FARME TEST 
	#WHEN 
	return None

def deEnv(filepathwithenv):
	print('deenv',filepathwithenv)
	envs = [('$DATA_PROD_PATH',os.getenv('DATA_PROD_PATH')),('$CACHE_PROD_PATH',os.getenv('CACHE_PROD_PATH')),('$HOME_PROD_PATH',os.getenv('HOME_PROD_PATH')),('$RENDER_PROD_PATH',os.getenv('RENDER_PROD_PATH'))]
	r = filepathwithenv
	for e in envs:
		if e[0] in filepathwithenv:
			print('replaces')
			r = filepathwithenv.replace(e[0],e[1])
	return r


def generate_rstexbin_aces(doConvert=True,bindAces=True): #0 - generate 1 - bind Aces 2 - bind srgb
	print("generate_rstexbin_aces()")
	import maya.cmds as cmds
	lw_platform , ossep = Lin_Win_and_sep() #return 0 is linux return 1 is windows
	#print(__file__) #D:/wxBrowser/mapy\mapy.py
	d = os.path.dirname(__file__)
	bins = os.path.dirname(d)+'/bin_portables'

	#print(bins,'bins')
	sel = cmds.ls(sl=True,long=True,type='file') or []
	if sel != []:
		all = sel
	else:
		#all = cmds.ls(type='file') or []
		print('SELECT FILE NODES TO CONVERT!!!!!!')
		return None
	userfolder = 'mt'
	evalFolder = os.getenv('CACHE_PROD_PATH')
	listfolders = evalFolder+'/aces_rstextbin/'
	folders = ''
	if os.path.isdir(listfolders):
		
		for fnames in os.listdir(listfolders):
			if os.path.isdir(listfolders+'/'+fnames):
				folders += fnames + ' | '

	if bindAces:
		userfolder = input_dialog('FolderNameforAcesTextures', 'mt - for path:\n$CACHE_PROD_PATH/aces_rstextbin/mt\n\n'+folders, 'mt')  #text - windowTitle; title -info for User; message - read/write user sring
	folderCache = 'aces_rstextbin/'+userfolder+'/' # need Query to cache data local
	folderVar = '$CACHE_PROD_PATH/'
	
	if not os.path.isdir(evalFolder+'/'+folderCache):
		recurciveFolderCreate(evalFolder+'/'+folderCache)
	listTextures = []
	for a in all:
		cmds.select(None)
		cmds.select(a)
		t = None
		try: t = cmds.getAttr(".fileTextureName")
		except:pass
		#try:cmds.setAttr(".colorSpace", "sRGB", type="string")
		#try: cmds.setAttr(".colorSpace", "gamma 1.8 Rec 709", type="string")
		#except: pass
		if t in listTextures:
			if bindAces:
				pass
			else:
				continue
		listTextures.append(t)
		if 'color' in t:
			print(t,' - File To process') 
			mask_worlds = ['.dds','Lenght','lenght','amound','amount','mask','height','scale','mashMasks']
			mask_worlds_int = 0
			for w in mask_worlds:
				if w in t:
					mask_worlds_int += 1
			if mask_worlds_int == 0: #to process
				#if not u'.dds' in t or not u'Lenght' in t or not u'lenght' in t or not u'amound' in t or not u'amount' in t or not u'mask' in t or not u'height' in t or not u'scale' in t or not u'mashMasks' in t : # mashMasks Lenght lenght amound mask height 
				#print(t)
				print('Processing......')
				atiffpath = None
				#print('mayapath',t)
				if 'rstexbin' in t:
					if folderVar in t: 
						if folderCache in t:# $CACHE_PROD_PATH/aces_rstextbin/_____MALYSH_assets_chars_ded_textures_color___ded__clothes_color.1003.rstexbin
							nwithoutfoldercache = t.replace(folderVar,'')
							nwithoutfoldercache = nwithoutfoldercache.replace(folderCache,'')
							nwithoutfoldercache = nwithoutfoldercache.replace('____','$DATA|PROD|PATH')
							dir_and_name = nwithoutfoldercache.split('___')
							#print('dir_name_name',dir_and_name)
							pathto = dir_and_name[0].replace('_','/')+'/'
							#print('pathto',pathto)
							t = pathto + dir_and_name[1]
							atiffpath = t.replace('.rstexbin','.tif')
					if atiffpath == None:
					#find tiff
						dt = os.path.dirname(t)
						ddt = os.path.dirname(dt)
						tn = os.path.basename(t)
						rtn = tn.replace('rstexbin','tif')
						tiffpath = ddt+ '/'+ rtn
						atiffpath = tiffpath
						#atiffpath = os.path.abspath(tiffpath)
						#if '\\' in atiffpath:
						#	atiffpath = atiffpath.replace('\\','/')
				else:
					atiffpath = t
					#atiffpath = os.path.abspath(t)
					#if '\\' in atiffpath:
					#	atiffpath = atiffpath.replace('\\','/')
				if atiffpath != None:
					atiffpath = atiffpath.replace('|','_')
					print('foundedTiff',atiffpath)
					udim = False
					if cmds.getAttr(".uvTilingMode") != 0:
						if '1001' in atiffpath:
							udim = True
						if '<UDIM>' in atiffpath:
							udim = True
							atiffpath = atiffpath.replace('<UDIM>','1001')

					dn = os.path.dirname(atiffpath)
					if ':' in dn:
						h = '$HOME_PROD_PATH'
						dn = dn.replace('C:/Work/Project',h).replace('D:/Work/Project',h).replace('E:/Work/Project',h)
					#print('dn',dn)

					bn = os.path.basename(atiffpath)
					rdn = dn.replace('/','_')
					rdn = rdn.replace('$DATA_PROD_PATH','____').replace('$CACHE_PROD_PATH','____').replace('$HOME_PROD_PATH','____').replace('$RENDER_PROD_PATH','____').replace('__dataServer_Project_','____').replace('__cacheserver_Project_','____').replace('__renderserver_Project_','____').replace('__dataserver_Project_','____')
					bignameTiff = rdn + '___' + bn
					bigpathRs = folderVar +folderCache+ bignameTiff.replace('.tif','.rstexbin')
					tiffpath = folderVar +folderCache+ bignameTiff
					listfiles = [(atiffpath,tiffpath,bigpathRs,1)]
					if udim:
						#print('Enb UDIM')
						for i in range(2,30):
							bnum = '1001'
							cnum = '10'+ str(i).zfill(2)
							#print('atiffpath',atiffpath)
							newtex = atiffpath.replace(bnum,cnum)
							#print('newtex',newtex)
							if os.path.isfile(deEnv(newtex)):
								print('appended_udims:',newtex)
								listfiles.append((atiffpath.replace(bnum,cnum),tiffpath.replace(bnum,cnum),bigpathRs.replace(bnum,cnum),0))
							
					#print(listfiles) #append Udim

					for conv in listfiles:
						weinput = deEnv(conv[0])
						wemidtiff = deEnv(conv[1])
						wers = deEnv(conv[2])
						print('weinput',weinput)
						print('wemidtiff',wemidtiff)
						print('wers',wers)

						if doConvert:
							config_ocio = bins + '/aces_1.0.3/config.ocio'
							vibranceFile = bins+'/aces_1.0.3/baked/maya/photoshop_vibrance75.csp'
							if lw_platform == 1: # windows
								print('win')
								oiiotool = bins + '/mrViewer-v5.3.1-Windows-64/bin/oiiotool.exe'
								redshiftTextureProcessor = bins+ '/redshift_texture_converter/redshiftTextureProcessor.exe'
								#/cacheserver/Project/lib/HOU/wxBrowser/bin_portables/mrViewer-v5.4.3-Linux-64/bin/oiiotool.sh IN --ociofiletransform /cacheserver/Project/lib/HOU/wxBrowser/bin_portables/aces_1.0.3/baked/maya/photoshop_vibrance100.csp --colorconfig COLORCONF --colorconvert srgb_texture ACEScg -o OUT
								srgb = True
								if srgb:
									print('Convert',weinput)
									cmd1 = [oiiotool, weinput,'--ociofiletransform', vibranceFile,'--colorconfig', config_ocio, '--colorconvert','srgb_texture', 'ACEScg','-o',wemidtiff]
									#cmd1 = [oiiotool, weinput, '--colorconfig', config_ocio, '--colorconvert','srgb_texture', 'ACEScg','-o',wemidtiff]
									print('  -> ',cmd1)
									cmd2 = [redshiftTextureProcessor,wemidtiff]
									print('  -> ',cmd2)
									if os.path.isfile(weinput):
										print('Found input file')
										res = subprocess.Popen(cmd1,shell=True)
										res.wait()
										res2 = subprocess.Popen(cmd2,shell=True)
										res2.wait()
										os.remove(wemidtiff)
										print('complited')
									else:
										print('NOT Found input file')
							else:
								#linux
								print('lin')
								oiiotool = bins + '/mrViewer-v5.4.3-Linux-64/bin/oiiotool.sh'
								redshiftTextureProcessor = bins+ '/redshift_texture_converter/bin/redshiftTextureProcessor.sh'
								srgb = True
								if srgb:
									print('Convert',weinput)
									cmd1 = [oiiotool, weinput,'--ociofiletransform', vibranceFile,'--colorconfig', config_ocio, '--colorconvert','srgb_texture', 'ACEScg','-o',wemidtiff]
									#cmd1 = [oiiotool, weinput, '--colorconfig', config_ocio, '--colorconvert','srgb_texture', 'ACEScg','-o',wemidtiff]
									print('  -> ',cmd1)
									cmd2 = [redshiftTextureProcessor,wemidtiff]
									print('  -> ',cmd2)
									if os.path.isfile(weinput):
										print('Found input file')
										#res = subprocess.Popen(cmd1,shell=True)
										os.system(' '.join(cmd1))
										#res.wait()
										#res2 = subprocess.Popen(cmd2,shell=True)
										#res2.wait()
										os.system(' '.join(cmd2))
										os.remove(wemidtiff)
										print('complited')
									else:
										print('NOT Found input file')
						if conv[3] == 1:#this master texture not udim contins
							if bindAces:
								print('to_file_path:',conv[2])
								settex = conv[2]
								if conv[2][-9:] != '.rstexbin':
									settex += '.rstexbin'
								if cmds.getAttr(".uvTilingMode") != 0:
									settex = settex.replace('1001','<UDIM>')
								cmds.setAttr(".fileTextureName",settex,type="string")
								cmds.setAttr(".colorSpace", "Raw", type="string")
							else: #bind to TIFF
								print('to_file_pathTIFF:',conv[0])
								settex = conv[0]
								if conv[0][-4:] != '.tif':
									settex += '.tif'
								if cmds.getAttr(".uvTilingMode") != 0:
									settex = settex.replace('1001','<UDIM>')
								cmds.setAttr(".fileTextureName",settex,type="string")
								cmds.setAttr(".colorSpace", "sRGB", type="string")



def setDisplayToACESRec709_disablePhotographicExposure():
	d = os.path.dirname(__file__)
	bins = os.path.dirname(d)+'/bin_portables'
	config_ocio = bins + '/aces_1.0.3/config.ocio'
	rsPosts = cmds.ls(type='RedshiftPostEffects') or []
	for rp in rsPosts:
		cmds.select(None)
		cmds.select(rp)
		cmds.setAttr(".outApiType", "RedshiftPostEffects", type="string")
		cmds.setAttr(".outApiClassification", "utility/general:rendernode/redshift/shader/lens:swatch/File", type="string")
		#cmds.setAttr(".version", -1)
		#cmds.setAttr(".clrMgmtDisplayMode", "RS_COLORMANAGEMENTDISPLAYMODE_OCIO", type="string")
		cmds.setAttr(".clrMgmtCustomGamma", 2.20000004768)
		cmds.setAttr(".clrMgmtOcioFilename", config_ocio, type="string")
		try:cmds.setAttr(".clrMgmtOcioView", "Rec.709", type="string")
		except:pass
		try:cmds.setAttr(".clrMgmtOcioDisplay", "ACES", type="string")
		except:pass
		cmds.setAttr(".clrCtrlEnable", 0)
		cmds.setAttr(".tonemapEnable", 0)
		try:cmds.setAttr(".outApiType", "RedshiftPostEffects", type="string")
		except: print ".outApiType passed"
		try:cmds.setAttr(".outApiClassification", "utility/general:rendernode/redshift/shader/lens:swatch/File", type="string")
		except: print ".outApiClassification passed"
		try:cmds.setAttr(".clrMgmtDisplayMode", "RS_COLORMANAGEMENTDISPLAYMODE_OCIO", type="string")
		except: print ".clrMgmtDisplayMode passed"
		try: cmds.setAttr(".clrMgmtCustomGamma", 2.20000004768)
		except: print ".clrMgmtCustomGamma passed"
		try:cmds.setAttr(".clrMgmtOcioFilename", "/cacheserver/Project/lib/HOU/wxBrowser/bin_portables/aces_1.0.3/config.ocio", type="string")
		except: print ".clrMgmtOcioFilename passed"
		try:cmds.setAttr(".clrMgmtOcioViewTransform", "Output - Rec.709", type="string")
		except: print ".clrMgmtOcioViewTransform passed"


def ToggleAcesCompinsationNodes():
	print("ToggleAcesCompinsationNodes()")
	import maya.cmds as cmds
	all = cmds.ls(type='RedshiftColorCorrection') or []
	firstToDisable = True
	fist_to_aces = None
	for a in all:
		if '_TO_ACES' in a:
			fist_to_aces = a
			break
	if fist_to_aces != None:
		if cmds.getAttr(a +'.gamma') == 1.0:
			firstToDisable = False
		if firstToDisable:
			print("Toggle Aces Compinsations to Disable")
			for a in all:
				cmds.setAttr(a+'.gamma', 1)
				cmds.setAttr(a+'.hue', 0)
				cmds.setAttr(a+'.saturation', 1)
				cmds.setAttr(a+'.level', 1)
		else:
			print("Toggle Aces Compinsations to Enable")
			for a in all:
				cmds.setAttr(a+'.gamma', 0.4025)
				cmds.setAttr(a+'.hue', 0)
				cmds.setAttr(a+'.saturation', 0.75)
				cmds.setAttr(a+'.level', 2.9)

def setFileNodesWithColorToRecGamma18():
	print("setFileNodesWithColorToRecGamma18()")
	allfilenodes = cmds.ls(long=True,type='file') or []
	firstToDisable = True
	fist_to_aces = None
	for a in allfilenodes:
		cmds.select(None)
		cmds.select(a)
		t = None
		try: t = cmds.getAttr(".fileTextureName")
		except:pass
		if 'color' in t:
			mask_worlds = ['.dds','Lenght','lenght','amound','amount','mask','height','scale','mashMasks']
			mask_worlds_int = 0
			for w in mask_worlds:
				if w in t:
					mask_worlds_int += 1
			if mask_worlds_int == 0: #to process
				#if not '.dds' in t or not 'Lenght' in t or not 'lenght' in t or not 'amound' in t or not 'amount' in t or not 'mask' in t or not 'height' in t or not 'scale' in t or not 'mashMasks' in t : # mashMasks Lenght lenght amound mask height 
				#print(t)
				#try:cmds.setAttr(".colorSpace", "sRGB", type="string")
				#setAttr "botanik_middle:file6.uvTilingMode" 3;
				if cmds.getAttr(".colorSpace") == "gamma 1.8 Rec 709":
					firstToDisable = False
				if firstToDisable:
					print("Toggle to gamma 1.8 Applied")
					try: cmds.setAttr(".colorSpace", "gamma 1.8 Rec 709", type="string")
					except: pass
				else:
					print("Toggle to sRGB Applied")
					try: cmds.setAttr(".colorSpace", "sRGB", type="string")
					except: pass

def deleteNameSpacesFromSelected():
	#DELETE NAME_SPACE_in_SELECTED
	selected = cmds.ls(sl=True, long=True) or []
	for s in selected:
		if ':' in s:
			mel.eval('rename "'+s+'" "'+s.split(':')[-1]+'";') # -1 comment


def renderSetupAnimation():
	print("renderSetupAnimation()")
	#set REDSHIFT
	cmds.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")

	#set AOV need Predelete
	cmds.setAttr("redshiftOptions.aovGlobalEnableMode", 1)

	for n in ["rsAov_BumpNormals","rsAov_Cryptomatte","rsAov_Custom", "rsAov_Depth","rsAov_DiffuseFilter"]:
		try:
			cmds.delete( n )
		except:
			pass
	cmds.rsCreateAov(type = 'Diffuse Filter')
	cmds.setAttr('rsAov_DiffuseFilter.enabled',1)
	cmds.rsCreateAov(type = 'Bump Normals')
	cmds.rsCreateAov(type = 'Cryptomatte')
	cmds.rsCreateAov(type = 'Depth')
	cmds.rsCreateAov(type = 'Custom')
	cmds.setAttr( "rsAov_Custom.name", "spec_eyes", type="string")
	cmds.setAttr("rsAov_Depth.filterMode", 3)

	# Exr Format beauty and crypta may be mormal_albedo
	cmds.setAttr("redshiftOptions.imageFormat", 1)
	cmds.setAttr("redshiftOptions.exrMultipart",1)
	cmds.setAttr("redshiftOptions.exrForceMultilayer", 1)

	#resolution 
	cmds.setAttr("defaultResolution.width",2048) 
	cmds.setAttr("defaultResolution.height",858)
	#cmds.setAttr("defaultResolution.pixelAspect",1)
	cmds.setAttr("defaultResolution.deviceAspectRatio",2.387)


	# GI 
	cmds.setAttr("redshiftOptions.secondaryGIEngine", 2)
	cmds.setAttr("redshiftOptions.primaryGIEngine", 4)
	cmds.setAttr("redshiftOptions.bruteForceGINumRays", 192)

	#Time
	startTime = int(cmds.playbackOptions(q=1, ast=1))
	endTime = int(cmds.playbackOptions(q=1, aet=1))
	cmds.setAttr("defaultRenderGlobals.animation",1)
	cmds.setAttr("defaultRenderGlobals.startFrame", startTime)
	cmds.setAttr("defaultRenderGlobals.endFrame", endTime)

	#Motion Blur
	cmds.setAttr("redshiftOptions.motionBlurEnable",1)
	cmds.setAttr("redshiftOptions.motionBlurFrameDuration", 0.75)
	cmds.setAttr("redshiftOptions.motionBlurDeformationEnable", 1)

	#Samples
	cmds.setAttr("redshiftOptions.unifiedMinSamples", 32)
	cmds.setAttr("redshiftOptions.unifiedMaxSamples", 386)
	cmds.setAttr("redshiftOptions.renderInCameraSpace", 1)
	cmds.setAttr("redshiftOptions.unifiedRandomizePattern",0)
	cmds.setAttr("redshiftOptions.unifiedMaxOverbright", 6)
	cmds.setAttr("redshiftOptions.glossyRayMaxOverbright", 1.4)
	cmds.setAttr("redshiftOptions.bucketSize", 64)

	# More samples for denoise disabled
	#setAttr "redshiftOptions.refractionSamplesOverrideEnable" 1;
	
	#setAttr "redshiftOptions.refractionSamplesOverrideMode" 1;
	
	#setAttr "redshiftOptions.refractionSamplesOverrideScale" 1.5;

	cmds.setAttr("redshiftOptions.reflectionSamplesOverrideEnable", 1)
	cmds.setAttr("redshiftOptions.reflectionSamplesOverrideMode", 1)
	cmds.setAttr("redshiftOptions.reflectionSamplesOverrideScale", 3)

	#Hair
	cmds.setAttr("redshiftOptions.hairTessellationMode", 1)
	cmds.setAttr("redshiftOptions.mpwHairEnabled", 0)

	#Dof
	#mel.eval('redshiftCreateGlobalShader RedshiftBokeh "rendernode/redshift/shader/lens" "bokeh";')
	#cmds.setAttr("rsBokeh1.dofOn", 0)

	#Find CAM to RENDER!!!!
	#Create Pparent Locator 
	#to Distance + Bokeh COC link
	#1308  547.98046875
	#2227 933
	l = cmds.ls('|cameras_grp')
	findmode = False
	animationCamera = u'perspShape'
	cams = cmds.ls(type='camera')
	if l == []:
		print ('custom camera')
		findmode = True
		for c in cams:
			if not c in [u'frontShape', u'perspShape', u'sideShape', u'topShape']:
				if 'sr' in c and 'ep' in c and 'sc' in c:
					print (c,'Found')
					animationCamera = c
	if not findmode:
		animationCamera = cmds.listRelatives(l, allDescendents=True, type='camera')[0]
	print (animationCamera)
	activedCamera = mel.eval('lookThru -q;')
	for c in cams:
	    cmds.setAttr(c+".renderable", 0)
	cmds.setAttr(animationCamera+".renderable", 1)

	print("RENDER SETUPED")

def PrintRefChecker():
	#t = r"""python /cacheServer/Project/lib/remoteExecution/lib/setup/maya/startMaya2017.py -rv 2644 -batch -file <REFNAME> -command '''python(\"execfile\\\"//cacheServer/Project/lib/HOU/mapyPipe/get_plugin_list\\\";\")''';"""
	if None == None:  # undisable this condition !!!!
		refs = mel.eval('ls -type reference')
		files = []
		not_ass_nodes = []
		i = 0
		for r in refs:
			try:
				reffilepath = cmds.referenceQuery(r,filename=True)
				if reffilepath[-1] != '}':
					if reffilepath not in files:
						files.append(reffilepath)
						i+=1
					print reffilepath
			except:
				not_ass_nodes.append(r)
				print r,'is not associated with a reference file.'
		print i
		div = i/7

		t = r"""python /cacheServer/Project/lib/remoteExecution/lib/setup/maya/startMaya2017.py -rv 2644 -batch -file <REFNAME> -command '''python( \"execfile( \\\"//cacheServer/Project/lib/HOU/mapyPipe/get_plugin_list/source.py\\\" ); \" ) '''&&"""
		print 'CMD ----------------------------------------------------------------------  :'
		ii = 0
		task = ''
		for f in files:
			cmd = t.replace('<REFNAME>',f)
			task += cmd
			ii += 1
			if ii == div:
				ii = 0
				print task + 'echo "joba_done"'
				task = ''
				print '\n--------------------------------------------------------------\n'

def reassigmMaterialFromNotes():
	sel = cmds.ls(sl=True,type='transform') or []
	for s in sel:
		cmds.select(None)
		cmds.select(s)
		note = None
		try:note = cmds.getAttr(s + '.notes')
		except:print('not_mat in Notes')
		if note != None:
			print(note)
			namenotns = s.split(':')[-1]
			mat = s.replace(namenotns,'')
			mat += note
			mel.eval('hyperShade -assign '+mat+';')

def isRef(shortnode):
	ref = True
	try:
		mel.eval('referenceQuery -filename -shortName '+shortnode+';')
	except:
		ref = False
	return ref

def setDATA_PROD_PATH():
	print('\n\nsetDATA_PROD_PATH()\n\n')
	allfilenodes = cmds.ls(long=True,type='file') or []
	for a in allfilenodes:
		cmds.select(None)
		if not isRef(a):
			cmds.select(a)
			t = None
			t = cmds.getAttr(".fileTextureName")
			udim = False
			if cmds.getAttr(".uvTilingMode") != 0:
				udim = True
			if '/MALYSH/' in t:
				tspl = t.split('/MALYSH/')
			elif '/default/' in t:
				tspl = t.split('/default/')
			else:
				break
			if udim:
				tspl[-1] = tspl[-1].replace('1001','<UDIM>')
			newt = '$DATA_PROD_PATH/MALYSH/' + tspl[-1]
			print(a,'->',newt)
			cmds.setAttr(".fileTextureName",newt,type="string")


'''
/cacheserver/Project/lib/HOU/wxBrowser/bin_portables/aces_1.0.3/config.ocio
/cacheserver/Project/lib/HOU/wxBrowser/bin_portables/aces_1.0.3/baked/maya/photoshop_vibrance100.csp

/cacheserver/Project/lib/HOU/wxBrowser/bin_portables/mrViewer-v5.4.3-Linux-64/bin/oiiotool.sh IMAGE --colorconfig /cacheserver/Project/lib/HOU/wxBrowser/bin_portables/aces_1.0.3/config.ocio



oiiotool = bins + '/mrViewer-v5.4.3-Linux-64/bin/oiiotool.sh'
								redshiftTextureProcessor = bins+ '/redshift_texture_converter/bin/redshiftTextureProcessor.sh'
								srgb = True
								if srgb:
									print('Convert',weinput)
									cmd1 = [oiiotool, weinput, '--colorconfig', config_ocio, '--colorconvert','srgb_texture', 'ACEScg','-o',wemidtiff]
								


cmds.setAttr("defaultRenderGlobals.currentRenderer", "redshift", type="string")
cmds.setAttr("redshiftOptions.aovGlobalEnableMode", 1)
cmds.rsCreateAov(type = 'Diffuse Filter')
cmds.setAttr('rsAov_DiffuseFilter.enabled',1)
cmds.setAttr("redshiftOptions.secondaryGIEngine", 2)
cmds.setAttr("redshiftOptions.bruteForceGINumRays", 196)
cmds.setAttr("redshiftOptions.mpwHairEnabled", 0)



file nodes 
for files detect udmis 
if tif or rstexbin -> find tiff

get datefiles for update append to name path unique to name
delete created  
constant folder
generate new 



generate_rstexbins_aces
if file selected only onde file generate

bind_all_to_rstexbin_aces

bind_all_to_tiff_srgb



E:/Work/Project/MALYSH/assets/sets/komnataMalysha/textures/color/cached/comnataMalysha_shkaf_color.rstexbin
DATA_PROD_PATH__MALYSH_assets_sets_komnataMalysha_textures_color___comnataMalysha_shkaf_color.tiff


#DELETE NAME_SPACE_in_SELECTED
#import maya.cmds as mc
#selected = mc.ls(sl=True, long=True) or []
#for s in selected:
#	if ':' in s:
#		mel.eval('rename "'+s+'" "'+s.split(':')[-1]+'";') # -1 comment


#Mel comon_render parms:
#setAttr "defaultRenderGlobals.ifp" -type "string" "fsffsfsadf";
#setAttr "defaultRenderGlobals.animation" 1;
#setAttr "defaultRenderGlobals.endFrame" 155;
#setAttr "defaultRenderGlobals.startFrame" 52;
#setAttr "redshiftOptions.imageFormat" 1;
#setAttr "defaultRenderGlobals.byFrameStep" 1;

unkown_nodes make selected
to Delete
all = cmds.ls(type='unknown',long=True) or []
cmds.select(None)
tosel = []
for u in all:
	try:
		ref = cmds.referenceQuery(u,referenceNode=True)
		print ref
	except:
		print u,'not in ref make selected'
		tosel.append(u)
		continue
cmds.select(tosel)



import maya.cmds as cmds

filterDyn = cmds.itemFilter(byType=('fluidEmitter','pointEmitter','rigidBody','nRigid','fluidShape','nParticle','nucleus','particle','nCloth','rigidConstraint'))
panel = cmds.outlinerPanel()
outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
cmds.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', filter=filterDyn , showShapes=True, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=True, showDagOnly=True, ignoreDagHierarchy=True, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter')






#OPEN and SAVE IMAGE in MAYA
#import imageio
#imageio.show_formats()

i1 = '/home/kirillovskih_i/Desktop/img.0056_0.0020.jpg'
i2 = '/home/kirillovskih_i/Desktop/img.0056_1.0020.jpg'
io = '/home/kirillovskih_i/Desktop/QT_SAVE_IMAGE.jpg'

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

def join_pixmap(p1, p2, mode=QtGui.QPainter.CompositionMode_SourceOver):
    s = p1.size().expandedTo(p2.size())
    result =  QtGui.QPixmap(s)
    result.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(result)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.drawPixmap(QtCore.QPoint(), p1)
    painter.setCompositionMode(mode)
    painter.drawPixmap(result.rect(), p2, p2.rect())
    painter.end()
    return result


picture1 = QtGui.QPixmap(i1)
picture2 = QtGui.QPixmap(i2)

p = join_pixmap(picture1, picture2, QtGui.QPainter.CompositionMode_SourceOver)

#out_pic = picture1 + picture2
#sc = picture1.scaled(400,400, Qt.KeepAspectRatio)
p.save(io,"jpg")
#picture2 = QImage(i2)
print(dir(picture1))





GEt intensity From BLENDER
bpy.data.scenes["Scene"].node_tree.nodes["RED"].inputs[1].default_value = 1.445

#bpy.data.node_groups["NodeGroup"].nodes["RED"].inputs[1].default_value = 5.94
#bpy.data.node_groups["NodeGroup"].nodes["GREEN"].inputs[1].default_value = 2.58
#bpy.data.node_groups["NodeGroup"].nodes["BLUE"].inputs[1].default_value = 3.31


createNode lambert -n "lambert2";
	rename -uid "58B3E388-452C-B3B3-45E5-C68ECB2097A5";
createNode shadingEngine -n "lambert2SG";
	rename -uid "4B638BFB-467E-BE6C-8BA6-C4B269573C54";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;


        #line 369 in /home/kirillovskih_i/lib/maya/Preferences/ReferenceHandle.py
        print("Load reference rfn", rfn)
        print("Load reference filename", filename)



'''



