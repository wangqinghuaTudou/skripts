import maya.cmds as cmds
from  an_Procedures.rivet import rivet
from an_Procedures.utilities import an_convertSliceToList, an_turnBasedUi
from an_classControllers import AnControllers  as ctrl
import re


def an_createControls():
    ctList = ['general', 'fk', 'sphere', 'switch', 'kross', 'circle',   'head', 'headAim',  'handIk',  'torso', 'shoulder', 'body', 'fkBody', 'legIk', 'curvedArrow']
    leyaut = an_turnBasedUi('ct', title ='Controllers criater',  stepsLabel =['Select type and click create', 'Add visProps to ct, and connect geometry'], stepNum=False)
    cmds.setParent(leyaut[0])
    cmds.rowColumnLayout(numberOfColumns=5, columnAttach=[1, 'left', 20],  columnWidth= [ (1, 55), (2, 100), (3, 120),   (4, 60),    (5, 30)], rs =[1, 2] )
    cmds.text( label=' Name: ' )
    cmds.textField( 'nameTF')
    cmds.optionMenuGrp('typeOM') #, columnWidth=[1, 40])
    for item in ctList:
        cmds.menuItem(label=item)
    cmds.checkBox('CHB', label='joint', v=True )
    cmds.button('pvRenRunButt', \
           label='Create', \
           width=80, \
           command='crCt()')
    cmds.separator(height=1, style='none')
    
    cmds.button('pvRenRunButt', \
       label='Connect', \
       width=80, \
       parent = leyaut[1], \
       command='add_visProps_to_ct()')
    
def add_visProps_to_ct(attr = "visProps"):
    ct, geo = cmds.ls(sl = True)
    cmds.addAttr(ct, ln=attr,  at="bool", keyable=True, defaultValue=True)
    cmds.connectAttr(ct+"."+attr, geo+".v")
    
 
def crCt():
    nameLocator=''
    if cmds.filterExpand (sm= 32):  # if eges selected
        list = cmds.filterExpand (sm= 32)
        e1 = re.findall('e\[(\d+)\]', list[0])[0]  
        e2 = re.findall('e\[(\d+)\]', list[1])[0]  
        nameObject =  list[0].split('.')[0]
        nameLocator = rivet(nameObject, [e1, e2], 'locator') 
        shp = cmds.listRelatives(nameLocator, s=1)
        cmds.delete(shp)
        cmds.select(nameLocator)
        
    name = cmds.textField( 'nameTF', q=True, tx=True)
    type = cmds.optionMenuGrp('typeOM', q=True, v=True)
    ct = ctrl(name+'_CT')
    if cmds.ls(  sl=True): ct.makeController ( type, size=1, offset =[0, 0, 0], orient="Y", pos=cmds.ls(sl=True)[0], posType='parent')
    else: ct.makeController ( type, size=1, offset =[0, 0, 0], orient="Y")
    if cmds.checkBox('CHB', q=True, v=True ): 
        jnt = cmds.joint(n=name+'_jnt')
        ofsGrp = cmds.group(jnt, n=name+'Ofs_grp')
        cmds.parent(ofsGrp, ct.oriGrp)
        cmds.setAttr (ofsGrp+'.t', 0, 0, 0)
        cmds.setAttr (ofsGrp+'.r', 0, 0, 0)
        for d in 't', 'r': 
            cmds.connectAttr(ct.name+'.'+d , jnt+'.'+d)
    if nameLocator:
        cmds.parent(ct.oriGrp, nameLocator)
        

 