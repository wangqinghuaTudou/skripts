import maya.cmds as cmds

from an_classSkeleton import AnSkeleton
from an_classSkeletonQuadro import AnSkeletonQuadro
from an_classNames import AnNames as chn
from an_classControllers import AnControllers  as ctrl

from anProcedures import *
from  an_rigAdditionalTools import *

from an_01_foldersHierarhy import  an_01_foldersHierarhy as an_01_foldersHierarhy
from an_02_bodyRig import  an_02_bodyRig as an_02_bodyRig
from an_03_headRig import  an_03_headRig as an_03_headRig
from an_04_limbRig import  an_04_limbRig as an_04_limbRig
from an_04_limbQuadroRig import  an_04_limbQuadroRig as an_04_limbQuadroRig
from an_05_neckRig import  an_05_neckRig as an_05_neckRig
from an_06_limbBendRig import  an_06_limbBendRig as an_06_limbBendRig
from an_06_limbBendQuadroRig import  an_06_limbBendQuadroRig as an_06_limbBendQuadroRig

from an_07_fingersRig import  an_07_fingersRig as an_07_fingersRig

''' Rig system for Bipedal or Quadruped characters'''

#''' _________________ general UI _____________ '''

def an_rigSys():
    win = "rigSysWin"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Rig system v1.00", width=420,  height=420, s=False, rtf=True, menuBar=True )
    cmds.columnLayout (  adjustableColumn=True, rowSpacing=1)
    cmds.radioButtonGrp('RigTypeRBG',  l='Rig type:  ', labelArray2=['Bipedal', 'Quadruped'], numberOfRadioButtons=2, sl= 1, height=30, cc='typeSwhitch()' )
    cmds.floatSliderGrp('ISG_gScale', label='Global scale:  ', field=True, min=0.1, max=10,  v=1 ,  enable= True , height=30 )
    tabs = cmds.tabLayout( )
    cmds.tabLayout( tabs, edit=True, tabLabel=( (skeletonTab(),  'Skeleton maker'),
                                                (an_riggingTab2(),  'Rigging'),
                                                (an_addToolsTab3(), 'Additional tools')))
    cmds.showWindow()


def typeSwhitch (): #procedure run when type swhitch
    tape = 'bip'     if cmds.radioButtonGrp('RigTypeRBG', q=True, sl=True )==1     else 'quad'
    if cmds.columnLayout ('rigCL', q=True, childArray=True,):
        cmds.deleteUI(cmds.columnLayout ('rigCL', q=True, childArray=True,))
    if tape == 'bip':   bipedalPanels()  # past panels in rig parts
    else:    quadrupedPanels ()
    com = 'an_Pers' if tape == 'bip' else 'an_PersQuadro' 
    cmds.button('delRigB',  e=True, c=com+'Rig("delRig")',w=202 )
    cmds.button('rigB', e=True, c=com+'Rig()',w=202 )

#''' _________________ Skeleton making UI _____________ '''

def skeletonTab():
    child1 = cmds.columnLayout (adjustableColumn=True, rowSpacing=5)
    cmds.canvas(  height=5 )
    
    for attr, label in zip(  ["jnt", "axis" , "ct" ],  ['Joint', 'Axis', 'Controller'] ):
        comand = "cmds.setAttr ('general_CT."    +attr+    "Vis', cmds.checkBoxGrp('"+attr+ "CHB', q=True,  v1=True))"
        cmds.checkBoxGrp( attr+'CHB',  ncb=1, label=label+ ' visibility:  ',   v1=True, en=cmds.objExists('general_CT.ctSize'), cc= comand   )
        
    if cmds.objExists('general_CT.ctSize'): cmds.attrFieldSliderGrp('AxisSizeFSG', l='Controller size:  ', min=0, max=5, attribute="general_CT.ctSize" )
    else: cmds.attrFieldSliderGrp('AxisSizeFSG', l='Controller size:  ', min=0, max=5, en=False)
        
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 210), (2, 210)] )
    cmds.button(l='Skeleton template', c='skeletonTabComand()')
    cmds.button(l='Final skeleton', c='AnSkeleton().createSceleton(miror=True)')
    for i in range(2): cmds.setParent( '..' )
    return child1


def skeletonTabComand(): #comand for button  'Skeleton template' 
    if cmds.radioButtonGrp('RigTypeRBG', q=True, sl=True )==1: AnSkeleton().skeletonRig()
    else: AnSkeletonQuadro().skeletonRig()
    for attr in  ["jnt", "axis" , "ct" ]:  cmds.checkBoxGrp( attr+'CHB',  e=True, en=True )
    cmds.attrFieldSliderGrp('AxisSizeFSG', l='Controller size:  ', e=True, min=0, max=5, attribute="general_CT.ctSize" )
    
    
#''' _________________ Rig making UI _____________ '''

def an_riggingTab2():
    child1 = cmds.columnLayout (adjustableColumn=True)
    cmds.frameLayout( label='Character parts setup:', bgc =[0,0,0]  )
    cmds.columnLayout ('rigCL', adjustableColumn=True)
    bipedalPanels()
    for each in xrange(1) :cmds.setParent( '..' )
    cmds.rowColumnLayout(nc =2   )
    cmds.button('delRigB',l='Delete rigging', c='an_PersRig("delRig")',w=202 )
    cmds.button('rigB',l='Rigging', c='an_PersRig()',w=202 )
    for each in xrange(3) :cmds.setParent( '..' )
    return child1

def an_PersRig(action='rig'):

    bodyProc = ['an_01_foldersHierarhy("'+action+'")' , 'an_02_bodyRig("'+action+'")', 'an_03_headRig("'+action+'")', 'an_05_neckRig("'+action+'")']
    limbProc = [ 'an_04_limbRig("'+action+'", "'+ x+'")' for x in  ('l_Arm', 'r_Arm',  'l_Leg', 'r_Leg')]
    bendProc = [ 'an_06_limbBendRig("'+action+'", "'+ x+'")' for x in  ('l_Arm', 'r_Arm',  'l_Leg', 'r_Leg')]
    fingerProc = [ 'an_07_fingersRig("'+action+'", "'+ x+'")' for x in  ('l_Arm', 'r_Arm' )]

    allProc =  bodyProc+limbProc+bendProc+fingerProc
    if action=='delRig':  allProc.reverse()
    for proc in allProc:
        if cmds.checkBox(proc.split('(')[0]+'CHB',   q = True,   value = True):
            eval(proc)
    ctrl('').an_setRotOrder()


def an_PersQuadroRig(action='rig'):

    bodyProc = ['an_01_foldersHierarhy("'+action+'")' , 'an_02_bodyRig("'+action+'")', 'an_03_headRig("'+action+'")', 'an_05_neckRig("'+action+'")']
    limbProc = [ 'an_04_limbQuadroRig("'+action+'", "'+ x+'")' for x in  ('l_Arm', 'r_Arm',  'l_Leg', 'r_Leg')]
    bendProc = [ 'an_06_limbBendQuadroRig("'+action+'", "'+ x+'")' for x in  ('l_Arm', 'r_Arm',  'l_Leg', 'r_Leg')]
    
    allProc =  bodyProc+limbProc+bendProc#+fingerProc
    if action=='delRig':  allProc.reverse()
    for proc in allProc:
        if cmds.checkBox(proc.split('(')[0]+'CHB',   q = True,   value = True):
            eval(proc)
    ctrl('').an_setRotOrder()



#Bipedal  pinel sets
def bipedalPanels ():
    an_rigPanel('an_01_foldersHierarhy', 'made', 'Folder hierarhy',options=False)
    an_rigPanel('an_02_bodyRig', 'made', 'Body rigging')
    an_rigPanel('an_03_headRig', 'made', 'Head rigging', options=False)
    an_rigPanel('an_04_limbRig', 'made', 'Limb rigging')
    an_rigPanel('an_05_neckRig', 'made', 'Neck rigging')
    an_rigPanel('an_06_limbBendRig', 'made', 'Limb Bend')
    an_rigPanel('an_07_fingersRig', 'made', 'Fingers rigging', options=False)
    an_rotOrderPanel()

#Quadruped  pinel sets
def quadrupedPanels ():
    an_rigPanel('an_01_foldersHierarhy', 'made', 'Folder hierarhy',options=False)
    an_rigPanel('an_02_bodyRig', 'made', 'Body rigging')
    an_rigPanel('an_03_headRig', 'made', 'Head rigging', options=False)
    an_rigPanel('an_04_limbQuadroRig', 'made', 'Legs rigging')
    an_rigPanel('an_05_neckRig', 'made', 'Neck rigging')
    an_rigPanel('an_06_limbBendQuadroRig', 'made', 'Limb Bend')
    an_rotOrderPanel()


def an_rigPanel(comand, action, v_text, options=True):  # made one laine panel for rig by parts
    cmds.rowColumnLayout(comand, nc=6, columnWidth=[(1, 6), (2, 10), (3, 100), (4, 120), (5, 120), (6, 45)], parent='rigCL')
    cmds.text ( '' , al='left' )#1
    cmds.checkBox(comand+'CHB', label='', value = True)#2
    cmds.text ( '  '+v_text , al='left' )#3
    cmds.button(l='Delete '+v_text.lower(), c=comand+"(action = 'delRig')" )#4
    cmds.button(l='Create '+v_text.lower(), c=comand+"(action = 'rig')" )#5
    if options: cmds.button(l='Options' , c=comand+"(action = 'option')" ) #5
    else: cmds.text ( ' ' , al='left' )
    cmds.setParent( '..' )

def an_rotOrderPanel():
    cmds.rowColumnLayout('rotOrderPanel', nc=6, columnWidth=[(1, 6), (2, 10), (3, 100), (4, 120), (5, 120), (6, 45)])
    for i in range(4):   cmds.text (' ' , al='left' )#1
    cmds.button(l='Set rotation order', c="ctrl('').an_setRotOrder()")#5
    cmds.setParent( '..' )



#''' _________________ Rig add tools UI _____________ '''

def an_addToolsTab3():
    child1 = cmds.columnLayout (adjustableColumn=True)

    an_jntVisibility ("UI")
    an_ctShapeTool("UI")
    for each in xrange(3) :cmds.setParent( '..' )
    return child1


