import maya.cmds as cmds
from an_classControllers import AnControllers  as ctrl
#from anProcedures import *

"""   an_rigAdditionalTools   """


def getSetCtShape(data={}):
    if data: 
        for ct in data.keys():  
           ctShapes = cmds.listRelatives(ct, s=True)
           for i in range(len(ctShapes)): 
                for p, pos in enumerate(data[ct][i]):
                   cmds.xform(ctShapes[i]+'.cv['+str(p)+']', t=pos , ws=True )
    else:
        ctList = cmds.ls(sl=True)
        data = {}
        for ct in ctList: 
            ctShapes = cmds.listRelatives(ct, fullPath=True, s=True)
            pos =  []
            for each in ctShapes: 
                pointsNum = cmds.getAttr (each+'.spans')+cmds.getAttr (each+'.degree') 
                pos.append( [cmds.xform(each+'.cv['+str(x)+']',  q=True, t=True, ws=True ) for x in range(pointsNum)] )
            data[ct]=pos
        return data
        
        
def parentCurveShape():
    sel = cmds.ls (sl=True)
    shape = cmds.listRelatives (sel[0], s=True, f=True)
    nShape = [ cmds.rename(shape[x], 'tmpName'+str(x)) for x in range(len (shape))] 
    for shp in nShape:
        pointsNum = cmds.getAttr (shp+'.spans')+cmds.getAttr (shp+'.degree') 
        pos = [cmds.xform(shp+'.cv['+str(x)+']',  q=True, t=True, ws=True ) for x in range(pointsNum)] 
        cmds.parent (shp , sel[1] , r=True , s=True ) 
        for p, pos in enumerate(pos):
                           cmds.xform(shp+'.cv['+str(p)+']', t=pos , ws=True )
    shape = cmds.listRelatives (sel[1], s=True)
    nShape = [ cmds.rename(shape[x], sel[1] + 'Shape'+str(x)) for x in range(len (shape))]                      
    cmds.select (sel[1], r=True)
    
def selectAllCT():
    
    def objTest (obj):   #filtre
        child = cmds.listRelatives(obj, c=True)[0]
        if cmds.nodeType (child)== 'nurbsCurve':  
            return True
        else: return False
        
    ctList = cmds.ls("*_CT")
    filtr = [x for x in ctList if objTest (x)]
    cmds.select(filtr) 

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


def  mirrorSelCT():
    for l_ct in  cmds.ls(sl=True):
        if 'l_' in l_ct: 
            r_ct = l_ct.replace('l_', 'r_')
            ctrl(l_ct).mirrorShape(r_ct)
                            

def an_ctShapeTool (function = ""):
    
    if function == "UI":
        cmds.frameLayout( label='Controllers shape tools:', bgc =[0,0,0], cll=True  )
        cmds.rowColumnLayout( nc=5, columnWidth=[(1, 74), (2, 90), (3, 80), (4, 80), (5, 80)])
        cmds.text ( ' Save to node : ' ,  al='left' )#1
        cmds.textField('RootTF' )#2
        cmds.button(l='Add selection ' , c='cmds.textField("RootTF", e=True, tx= cmds.ls(sl=True)[0])' )#3
        cmds.button(l='Load shapes' , c='an_ctShapeTool( function = "get" )' )#4
        cmds.button(l='Save shapes ' , c='an_ctShapeTool( function = "save" )' )#5
        for each in xrange(2) :cmds.canvas()
        cmds.button(l='Parent curve' , c='parentCurveShape()')#2
        cmds.button(l='Select all CT' , c='selectAllCT()')#2
        cmds.button(l='Mirror shape' , c='mirrorSelCT()' )#3

        for each in xrange(2) :cmds.setParent( '..' )

    if function == "get": getSetCtShape(an_saveLoadData(obgect = cmds.textField('RootTF', q=True, tx=True )))
    if function == "save":  an_saveLoadData(getSetCtShape(), obgect = cmds.textField('RootTF', q=True, tx=True ))# save to obj 
    
    

    
                       