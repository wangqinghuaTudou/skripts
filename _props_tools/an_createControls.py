import maya.cmds as cmds
from  anProcedures import  *
from an_classControllers import AnControllers  as ctrl

def an_createControls():
    ctList = ['general', 'fk', 'sphere', 'switch', 'kross', 'circle',   'head', 'headAim',  'handIk',  'torso', 'shoulder', 'body', 'fkBody', 'legIk', 'curvedArrow']
    leyaut = an_turnBasedUi('ct', title ='Controllers criater',  stepsLabel =['select type and click create', ])[0]
    cmds.setParent(leyaut)
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
 
def crCt():
    nameLocator=''
    if cmds.filterExpand (sm= 32):  # if eges selected
        list = cmds.filterExpand (sm= 32)
        e1 =  list[0].split('[')[1].split(']')[0]
        e2 =  list[1].split('[')[1].split(']')[0]
        nameObject =  list[0].split('.')[0]
        nameLocator = an_rivet(nameObject, str(e1), str(e2)) 
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
        

 