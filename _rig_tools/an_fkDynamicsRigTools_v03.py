
import maya.cmds as cmds
from anProcedures import  an_childCapture, an_fkRig, an_connectReversAttr, an_makeDynamicsCurve, an_delSys, an_connectRigVis, an_jntOnCurv
from An_Controllers import An_Controllers as ctrl
from CharacterNames import CharacterNames as chn

def an_fkDynamicsRigTools_v03 ():
        win = "DynamicsRigv4"
        if  cmds.window (win, exists=True ): cmds.deleteUI (win)
        cmds.window (win, t="Fk rigging tools    v3.1", width=388,  height=210, s=False, rtf=True, menuBar=True )
        cmds.columnLayout ( adjustableColumn=True)
        cmds.text ('        -Create fk and dynamics rigging to joints chain. Select start then end joints.  ', h=15,  al='left')
        cmds.text ('        -Starting bone should be the parent for fixing whole system', h=15, al='left')
        cmds.text ('        -To delete, select the rigging group, and then click "delete"', h=15, al='left')
        cmds.canvas( height=5 )
        cmds.textFieldGrp ( 'TFGpfx', label="Prefix :   ", text="")
        cmds.canvas( height=5 )

        cmds.checkBoxGrp('CHBdyn', label='Made dynamics :   ' )
        cmds.canvas( height=5 )

        cmds.checkBoxGrp('CHBik', label='Made spline ik :   ',   changeCommand= "cmds.intFieldGrp('IFGnum',e=True,enable=cmds.checkBoxGrp('CHBik', q=True, v1=True))" )
        cmds.canvas( height=5 )
        cmds.intFieldGrp('IFGnum', numberOfFields=1, label='Number of bones  :   ',  value1=20, enable=False,  )

        cmds.canvas( height=15 )
        cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 142), (2, 120), (3, 120)] )
        cmds.canvas( height=5 )
        cmds.button (l="Delete dynamics rig", c="an_delDynamicsRig()")
        cmds.button(l="Make dynamics rig", c= 'an_doDynamicsRig_v03(fkCtSize=3)' )#4
        cmds.showWindow()

def an_delDynamicsRig(): an_delSys(cmds.ls (sl=True)[0])

def an_doDynamicsRig_v03(fkCtSize=3):

    pfx = cmds.textFieldGrp ( 'TFGpfx', q=True, text=True)
    jnts = an_childCapture(cmds.ls(sl=True))
    parentObj = cmds.listRelatives (jnts[0], p=True)
    rigGrp = cmds.group ( em=True, n= pfx+'Rig_grp'  )

    dynJnts, delSysObjects, rigVisObjects =[],[], []   #create spline ik dynamics jnt
    if cmds.checkBoxGrp('CHBdyn', q=True, v1=True):
        for i, jnt in enumerate(cmds.duplicate( jnts[0], renameChildren = True )):
            parts=chn(jnts[i]).divideName()
            newName = cmds.rename (jnt,  parts[0]+'din'+parts[1].capitalize()+parts[2])
            dynJnts.append(newName)
        delSysObjects.append(dynJnts[0])
        rigVisObjects.append(dynJnts[0])

    ctObjects, fkRigGrp = an_fkRig( jnts, pfx, fkCtSize)  #create fk rig
    cmds.parentConstraint (parentObj[0], fkRigGrp,  mo=True)
    cmds.parent(  fkRigGrp,  rigGrp  )
    delSysObjects.append(fkRigGrp)

    if cmds.checkBoxGrp('CHBdyn', q=True, v1=True):

        for i, ctObj in enumerate(ctObjects):
            cmds.connectAttr (dynJnts[i]+'.r', ctObj.conGrp+'.r')
        deg = 1 if len(jnts)<4 else 3

        vCurve = cmds.curve(n = pfx+"_crv",  p=[cmds.xform  (jnt, q=True, t=True, ws=True) for jnt in jnts ], d=deg )#create dynamics curve
        if len(jnts)<4: cmds.rebuildCurve (vCurve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=0, d=2, tol=0.01)
        dynCurve, folicle, hairSysShape = an_makeDynamicsCurve (vCurve)

        cmds.addAttr (ctObjects[0].name, ln="dynamic",  at="bool", keyable=True)
        for v1, v2 in [(1, 3), (0, 1)]: cmds.setDrivenKeyframe ( hairSysShape+".simulationMethod",  cd=ctObjects[0].name+".dynamic",  dv=v1, v=v2 )
        folicleSysShape = cmds.listRelatives (folicle, s=True)[0]
        for v1, v2 in [(1, 2), (0, 0)]: cmds.setDrivenKeyframe ( folicleSysShape+".simulationMethod",  cd=ctObjects[0].name+".dynamic",  dv=v1, v=v2 )

        cmds.addAttr (ctObjects[0].name, ln='dynamicWeight', min=0, dv=1, max=1 , keyable=True)
        an_connectReversAttr (ctObjects[0].name+'.'+'dynamicWeight', hairSysShape+'.'+'startCurveAttract')
        cmds.parentConstraint (parentObj[0], folicle,  mo=True)
        cmds.setAttr (folicle  + ".pointLock", 1)
        ikHandl = cmds.ikHandle  (n=pfx+'_din_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=dynJnts[0], ee= dynJnts[-1], c=dynCurve)
                        #advans tw  control
        cmds.setAttr (ikHandl[0]+".dTwistControlEnable", 1)
        cmds.setAttr (ikHandl[0]+".dWorldUpType", 3)
        cmds.setAttr (ikHandl[0]+".dWorldUpAxis", 3)
        cmds.setAttr (ikHandl[0]+".dWorldUpVector", 0, 0, 1)
        cmds.connectAttr (parentObj[0]+'.worldMatrix[0]',  ikHandl[0]+'.dWorldUpMatrix')

        for arg in [folicle, hairSysShape, ikHandl[0], dynCurve]:  rigVisObjects.append(arg)
        for arg in [folicle, hairSysShape, ikHandl[0], dynCurve]:  delSysObjects.append(arg)

        cmds.parent(   cmds.listRelatives (folicle, p=True)[0], cmds.listRelatives (dynCurve, p=True)[0], cmds.listRelatives (hairSysShape, p=True)[0],  ikHandl[0],  rigGrp  )

    if cmds.checkBoxGrp('CHBik', q=True, v1=True):

        deg = 1 if len(jnts)<4 else 3
        v_curve = cmds.curve ( n=pfx+'_curve',  p=[cmds.xform (x, q=True, ws=True, t=True) for x in jnts], d=deg)
        if len(jnts)<4:
            cmds.rebuildCurve (v_curve, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=0, d=2, tol=0.01)
            skinClusterName = cmds.skinCluster(parentObj+jnts, v_curve, tsb=True)[0]
        else: skinClusterName = cmds.skinCluster(jnts, v_curve, tsb=True)[0]
        splinJointName, ikHandl = an_jntOnCurv(v_curve, jntNum = cmds.intFieldGrp('IFGnum', q=True, v1=True), stretchable=True, pfx=pfx)
        cmds.parent ( v_curve, ikHandl[0], rigGrp)

        #advans tw  control
        cmds.setAttr (ikHandl[0]+".dTwistControlEnable", 1)
        cmds.setAttr (ikHandl[0]+".dWorldUpType", 4)
        cmds.setAttr (ikHandl[0]+".dWorldUpAxis", 3)
        cmds.setAttr (ikHandl[0]+".dWorldUpVector", 0, 0, 1)
        cmds.setAttr (ikHandl[0]+".dWorldUpVectorEnd", 0, 0, 1)
        cmds.connectAttr (ctObjects[0].name+'.worldMatrix[0]',  ikHandl[0]+'.dWorldUpMatrix')
        cmds.connectAttr (ctObjects[-1].name+'.worldMatrix[0]',  ikHandl[0]+'.dWorldUpMatrixEnd')


        for arg in [v_curve, ikHandl[0]]:  rigVisObjects.append(arg)
        for arg in [v_curve, ikHandl[0], splinJointName[0] ]:  delSysObjects.append(arg)

    if cmds.checkBoxGrp('CHBik', q=True, v1=True) or cmds.checkBoxGrp('CHBdyn', q=True, v1=True):
        an_connectRigVis (rigGrp, rigVisObjects)
    an_delSys(rigGrp, delSysObjects)








