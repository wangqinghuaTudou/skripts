"""
Main Procedure:
    an_makeInfluenceObjScalably()

Creation Date:
    april 27, 2016

Authors:
    Belyaev Andrey
    andreikin@mail.ru
    www.3drigging.com
Description:
    The script allows you to remove disadvantage of influence objects - the inability to scale

Installation:

    1. Copy the [an_insertOffset] to your local user/scripts folder
		 		example: ..\my documents\maya\scripts\
	2. Start Maya
	4. Type:    import an_makeInfluenceObjScalably
                from an_makeInfluenceObjScalably import *
                an_makeInfluenceObjScalably()
	   into the Maya Script Editor (Pithon mod), and hit enter.

How to Use:
    1. Select one channel in the channel box
	2. Select the node type and its insert position
	3. Press "make connection"
	4. To delete nod - Select its insert position, select the same attribut in the channel box and press "delete connection"

Notes:
    **** When you choose "reverse" node, "Offset" attribute is not created.
    **** Be careful when working with rotation attributes (because the Maya inserts "unitConversion" nodes automatically)

Comments or suggestions? E-mail me!!!
Good luck!!!


*************************************************************************************************************************
 version History
*************************************************************************************************************************
	v2.0
	- Add script description.
	- Add opportunity to insert a "Revers" node.
	- Add comments in the code.

*************************************************************************************************************************
 Modify at your own risk
"""

import maya.cmds as cmds

def makeInfluenceObjScalablyUi():
    win = "influenceObjScalablyUi"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Make influence object scalably v1.0", width=420,  height=50, s=True, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout ('columnLayoutName', adjustableColumn=True)
    cmds.frameLayout (label=" Operating order :", borderStyle="etchedIn", cll=0, w=424, bgc= [0, 0, 0])
    cmds.columnLayout (height= 200, width = 410)
    cmds.canvas( height=1 )
    cmds.text (l="         Add two nodes of transformation: ", al="left", font= "boldLabelFont")
    bc = "cmds.textFieldButtonGrp ('TFBG_Sc', e=True, tx=  cmds.ls (sl=True)[0])"
    cmds.textFieldButtonGrp ('TFBG_Sc', l="Scalable (controller or group):",  bl="<<Add selected",  cw = [(1, 180), (2, 146)],  bc = bc )
    bc = "cmds.textFieldButtonGrp ('TFBG_nonSc', e=True, tx=  cmds.ls (sl=True)[0])"
    cmds.textFieldButtonGrp ('TFBG_nonSc', l="Nonscalable (group):",  bl="<<Add selected",  cw = [(1, 180), (2, 146)],  bc = bc )
    cmds.rowColumnLayout (nc=2, cw=[(1, 210), (2, 208)])
    cmds.canvas()
    cmds.button   (l="Make influence object scalably",   c="an_makeScalably()" )
    cmds.showWindow (win)

def an_makeScalably():
    geometry = cmds.ls(sl=True)[0]
    scalableGrp = cmds.textFieldButtonGrp ('TFBG_Sc', q=True,  text=True)
    nonScalableGrp = cmds.textFieldButtonGrp ('TFBG_nonSc', q=True,  text=True)
    an_makeInfluenceObjScalably(geometry, [scalableGrp, nonScalableGrp])

def an_makeInfluenceObjScalably(geometry, groups = []):
    tmp = geometry.split('_')
    pfx = tmp[0]+'_'+tmp[1]    if len (tmp)==3 else tmp[0]
    skinClaster =  cmds.ls (cmds.listHistory (geometry, pdo=1), type='skinCluster')[0]     # get curve skin Cluster Name
    skinJntList = cmds.ls ( cmds.listHistory (skinClaster, levels=1), type='transform')    # get curve skin Jnt List
    shape = cmds.listRelatives(geometry, s=True)[0]     # get geo shape
    vNum = cmds.polyEvaluate(geometry, v=True)  # get vertex number

    driverGrp = cmds.group(em=True, n=pfx+'Driver_grp')# driver grp
    nonScaleGrp = cmds.group(em=True, n=pfx+'NonScale_grp')# non scale grp

    driverJnt, staticJnt = [],[]   # creation of two groups with joints wich echo position of the bones of the curve
    for i, eachJnt in enumerate( skinJntList):
        cmds.select (cl =True)
        drJnt = cmds.joint(n=pfx+'Driver0'+str(i)+'_jnt')
        cmds.delete (cmds.pointConstraint (eachJnt, drJnt ))
        cmds.parent (drJnt, driverGrp)
        cmds.parentConstraint (eachJnt, drJnt, mo=True )
        driverJnt.append(drJnt)

        stJnt = cmds.joint(n=pfx+'Static0'+str(i)+'_jnt')
        cmds.parent (stJnt, nonScaleGrp)
        cmds.connectAttr (drJnt+'.t', stJnt+'.t')
        cmds.connectAttr (drJnt+'.r', stJnt+'.r')
        staticJnt.append(stJnt)

    weight = []      #curve points weights storage
    for i in range (vNum):  weight.append( cmds.skinPercent( skinClaster, geometry+'.vtx['+str(i)+']', query=True, value=True )) #get weights

    cmds.skinCluster (shape, e=True, ub=True )               #detach skin
    newSkinClusterName = cmds.skinCluster(staticJnt, geometry, tsb=True)[0] #new skin to static jnt

    for i in range (vNum):  # set skin weight
        cmds.skinPercent( newSkinClusterName, geometry+'.vtx['+str(i)+']', transformValue=zip(staticJnt,weight[i]))

    skinClusterConnection = cmds.connectionInfo(shape+'.worldMesh[0]', destinationFromSource=True)[0].replace('driverPoints', 'basePoints') # get base object
    baseObjShape = cmds.connectionInfo(skinClusterConnection, sourceFromDestination=True).split('.')[0]
    baseObj = cmds.listRelatives(baseObjShape, p=True)[0]

    for geo in [baseObj, geometry]: cmds.parent (geo, driverGrp)

    if groups[0]: cmds.parent ( driverGrp, groups[0])
    if groups[1]: cmds.parent ( nonScaleGrp, groups[1])

    return driverGrp, nonScaleGrp













