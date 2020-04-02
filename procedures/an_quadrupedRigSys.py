
import maya.cmds as cmds
from An_Skeleton import  An_Skeleton as An_Skeleton
from CharacterNames import CharacterNames as chn
from An_Controllers import An_Controllers  as ctrl 
from anProcedures import *
from  an_rigAdditionalTools import *
from an_01_foldersHierarhy import  an_01_foldersHierarhy as an_01_foldersHierarhy

from an_bipedalRigSys import an_addToolsTab3


def an_quadrupedRigSys():
    win = "qrsSysWin"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Quadruped Rig System v1.00", width=420,  height=390, s=False, rtf=True, menuBar=True )
    cmds.columnLayout ('columnLayoutName'  , adjustableColumn=True)
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.tabLayout( tabs, edit=True, tabLabel=( (an_skeletonTab(), 'Skeleton maker'), 
                                                (an_riggingTab2(), 'Rigging'),
                                                (an_addToolsTab3(), 'Additional tools')) )
    cmds.showWindow()


def an_skeletonTab():
    child1 = cmds.columnLayout (adjustableColumn=True)
    cmds.text ('-Create a template and place the joints at the appropriate places',h=30)
    cmds.button(l='Skeleton template', c='an_SkeletonTemplate("template")')
    cmds.frameLayout( label='Template display mode:', bgc =[0,0,0] ) 
    cmds.canvas( height=5 )
    if cmds.objExists('general_CT.axesSize'):
        cmds.checkBoxGrp( 'AxisCHB',   numberOfCheckBoxes=1, label='Axis visibility:  ', cc = "an_chekBoxSwitch('AxisCHB')",  v1=False)
        cmds.attrFieldSliderGrp('AxisSizeFSG', l='Axis size:  ', min=0, max=10, attribute="general_CT.axesSize" )  
        cmds.checkBoxGrp( 'JointCHB' ,  numberOfCheckBoxes=1, label='Joint visibility:  ', cc= "an_chekBoxSwitch('JointCHB')",  v1=False )
        cmds.checkBoxGrp( 'ctCHB' ,  numberOfCheckBoxes=1, label='Controllers visibility:  ', cc= "an_chekBoxSwitch('ctCHB')",  v1=True )
        cmds.attrFieldSliderGrp('ctSizeFSG', l='SpheresSize:  ', min=0, max=10, attribute="general_CT.SpheresSize" ) 
        cmds.radioButtonGrp('HandRBG', label='Hand axis: ', labelArray2=['Fingers', 'Revers'], numberOfRadioButtons=2, sl= 1, onCommand1 = 'an_axisSwitch("handOn")', onCommand2 = 'an_axisSwitch("handRevers")')
        cmds.radioButtonGrp('LegRBG', label='Leg axis: ', labelArray2=['Leg', 'Revers'], numberOfRadioButtons=2, sl= 1, onCommand1 = 'an_axisSwitch("legOn")', onCommand2 = 'an_axisSwitch("legRevers")' )
    cmds.canvas( height=5 )
    cmds.setParent( '..' )
    cmds.canvas( height=5 )
    cmds.frameLayout( label='Final skeleton option:', bgc =[0,0,0]  )
    cmds.canvas( height=5 )     
    cmds.checkBoxGrp( 'mirrorCHB' ,  numberOfCheckBoxes=1, label='Mirror joint:  ', cc= "an_chekBoxSwitch('JointCHB')",  v1=True)
    cmds.button(l='Final skeleton', c='an_SkeletonTemplate("skelet")')
    for each in xrange(2) :cmds.setParent( '..' )
    return child1
    
########################################################


def an_riggingTab2():
    child1 = cmds.columnLayout (adjustableColumn=True)
    cmds.frameLayout( label='Character parts setup:', bgc =[0,0,0]  )
    cmds.columnLayout ('rigCL', adjustableColumn=True)
    
    #an_rigPanel('an_01_foldersHierarhy', 'made', 'Folder hierarhy',options=False)
    #an_rigPanel('an_02_bodyRig', 'made', 'Body rigging')
    #an_rigPanel('an_03_headRig', 'made', 'Head rigging', options=False)
    #an_rigPanel('an_04_limbRig', 'made', 'Limb rigging')
    #an_rigPanel('an_05_neckRig', 'made', 'Neck rigging') 
    #an_rigPanel('an_06_limbBendRig', 'made', 'Limb Bend')
    #an_rigPanel('an_07_fingersRig', 'made', 'Fingers rigging', options=False) 
    #an_rotOrderPanel()
    
    for each in xrange(1) :cmds.setParent( '..' )
    cmds.rowColumnLayout(nc =2   )
    cmds.button(l='Delete rigging', c='an_PersRig("delRig")',w=202 )
    cmds.button(l='Rigging', c='an_PersRig()',w=202 )
    
    for each in xrange(3) :cmds.setParent( '..' )
    return child1

def an_rigPanel(comand, action, v_text, options=True):
    cmds.rowColumnLayout(comand, nc=6, columnWidth=[(1, 6), (2, 10), (3, 100), (4, 120), (5, 120), (6, 45)])
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
    
 

#______________________________________________________________________________________________________________________
"""
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


########################################################


     
def an_axisSwitch(action):
    actArm, actLeg = [], []
    if action == 'handOn': actArm = [1, 0]
    if action == 'handRevers': actArm = [0, 1]
    if action == 'legOn': actLeg = [1, 0]
    if action == 'legRevers': actLeg = [0, 1] 
    if actArm: 
        cmds.setAttr ("general_CT.handAxisVisibility", actArm[0])
        cmds.setAttr ("general_CT.handReversVisibility", actArm[1])        
    if actLeg: 
        cmds.setAttr ("general_CT.legAxisVisibility", actLeg [0])
        cmds.setAttr ("general_CT.legReversVisibility", actLeg [1])       

########################################################
     
def an_chekBoxSwitch(chBox):
    attr = '.controllersVisibility'
    if  chBox =='AxisCHB':
        attr = '.axisVisibility'  
    if  chBox =='JointCHB':
        attr = '.jointVisibility'
    if cmds.checkBoxGrp( chBox, q=True,  v1=True):  cmds.setAttr ("general_CT"+attr, 1)
    else:   cmds.setAttr ("general_CT"+attr, 0)       
   
def an_SkeletonTemplate(aktion):
    obj = An_Skeleton()
    if aktion == 'template':  
        obj.templateCtrl()
    if aktion == 'skelet':
        obj.skeletFromTemplate()
        if cmds.checkBoxGrp( 'mirrorCHB', q=True,  v1=True): 
            [cmds.mirrorJoint (x, myz=True,  mb=True, sr= ["l_", "r_"]) for x in [obj.shoulderJnt, obj.hipJnt, obj.legRevers[0], obj.armRevers[0]] ]
    an_bipedalRigSys()         
   
def an_jntVisibility( function = ""):
    if function == "UI":
        cmds.frameLayout( label='Joints visibility:', bgc =[0,0,0], cll=True  )
        cmds.rowColumnLayout( nc=5, columnWidth=[(1, 74), (2, 90), (3, 80), (4, 80), (5, 80)])
        cmds.text ( '  Switch CT : ' ,  al='left' )#1
        cmds.textField('SwitchTF', tx='switch_CT' )#2
        cmds.button(l='Add selection ' , c='cmds.textField("SwitchTF", e=True, tx= cmds.ls(sl=True)[0])' )#3
        cmds.button(l='Hide' , c='an_jntVisibility( function = "Hide" )' )#4
        cmds.button(l='Show ' , c='an_jntVisibility( function = "Show" )' )#5
        for each in xrange(2) :cmds.setParent( '..' )
    else:
        sel = cmds.ls(sl=True)
        switch = cmds.textField("SwitchTF", q=True, tx=True )
        if not cmds.objExists(switch+'.jntVis'):
            cmds.addAttr (switch, ln="jntVis", at="enum", en="off:on", keyable=False)
            revers = cmds.createNode  ("reverse", n='jntVisRevers')
            cmds.connectAttr (switch+'.jntVis', revers+".inputX")    
        for each in sel:
            if cmds.objectType (each, isType="joint" ):
                if not cmds.connectionInfo (each+".overrideEnabled", id=True ):
                    cmds.connectAttr ("jntVisRevers.outputX", each+".overrideEnabled")                
                if not cmds.connectionInfo (each+".overrideVisibility", id=True ): 
                    cmds.connectAttr (switch+'.jntVis', each+".overrideVisibility")        
        if function == "Hide": cmds.setAttr (switch+'.jntVis', 0)
        if function == "Show": cmds.setAttr (switch+'.jntVis', 1)

def an_ctShapeTool (function = ""):
    if function == "UI":
        cmds.frameLayout( label='Controllers shape tools:', bgc =[0,0,0], cll=True  )
        
        cmds.rowColumnLayout( nc=5, columnWidth=[(1, 74), (2, 90), (3, 80), (4, 80), (5, 80)])
        cmds.text ( ' Save to node : ' ,  al='left' )#1
        cmds.textField('RootTF' )#2
        cmds.button(l='Add selection ' , c='cmds.textField("RootTF", e=True, tx= cmds.ls(sl=True)[0])' )#3
        cmds.button(l='Load shapes' , c='an_ctShapeTool( function = "get" )' )#4
        cmds.button(l='Save shapes ' , c='an_ctShapeTool( function = "save" )' )#5
        for each in xrange(3) :cmds.canvas()
        cmds.button(l='Select all CT' , c='cmds.select("*_CT")')#2
        cmds.button(l='Mirror shape' , c='ctrl(cmds.ls(sl=1)[0]).mirrorShape(cmds.ls(sl=1)[1])' )#3        
        
        for each in xrange(2) :cmds.setParent( '..' )
    if function == "get": getSetCtShape(an_saveLoadData(obgect = cmds.textField('RootTF', q=True, tx=True ))) 
    if function == "save":  an_saveLoadData(getSetCtShape(), obgect = cmds.textField('RootTF', q=True, tx=True ))# save to obj
        
 
"""                
        
 


	   
	   

	   


 
	   
    
	   
	   
	   
	   
	   
	   
	   
	   
	   
 