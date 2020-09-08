
 

import maya.cmds as cmds
from an_Procedures.utilities import an_turnBasedUi
import maya.mel as mm


def an_dynRope ():
    leyouts = an_turnBasedUi('dynRopeUi', title ='dynRope',  stepsLabel =['Make rope',])
    cmds.columnLayout ('bridgLayout', adjustableColumn=True, p=leyouts[0]) 
    cmds.canvas(h=10)
    cmds.text('       Select curve and prese "Create rope"',   al='left')
    cmds.canvas(h=10)
    cmds.textFieldGrp('pfx_TFG', label='Prefix : ', text='rope_1'  )
    cmds.canvas(h=3)
    cmds.intSliderGrp('num_ISG', field=True, label='Division number : ', minValue=10, maxValue=500, fieldMinValue=10, fieldMaxValue=500, value=150 )
    cmds.button( label='Create rope', c='doDynRope(0)')

#an_dynRope ()


def an_jntOnCurvNonspline (curveName, jntNum = 10, pfx='',  geo=True):
    
    cmds.select (cl=True,  sym =True)
    pfx = curveName+'ChSys' if not pfx else pfx
    curveShape = cmds.listRelatives(curveName, s=True)[0]
    jointName = range(jntNum+1)
     
    jntGrp = cmds.group(n=pfx+'Joints_grp', em=True)
    rigGrp = cmds.group(jntGrp, n=pfx+'Rig_grp')
    
    jointName = range(jntNum)
    for index, string in enumerate(range(jntNum)):
    		 jointName[index]= cmds.joint (r=True , n=pfx+str(index)+'_jnt', p= [cmds.arclen(curveName)/(jntNum-1), 0, 0])
    if geo:
        geo = cmds.polyCylinder( r=cmds.arclen(curveName)/jntNum/8, h=cmds.arclen(curveName),  sy= jntNum-1 , sx=6, ax=[1, 0, 0])[0]
        cmds.delete(cmds.pointConstraint(jointName[0],jointName[-1], geo))
        cmds.skinCluster(jointName, geo, tsb=True, normalizeWeights=True)
    
    for index, string in enumerate(range(jntNum)):
        cmds.select (cl=True,  sym =True)
        #if not index==0: cmds.parent(jointName[index], w=True)
        
        cmds.parent(jointName[index], jntGrp)
        poci = cmds.createNode( 'pointOnCurveInfo', n=pfx+str(index)+'_poci')
        cmds.setAttr (poci+".turnOnPercentage", 1)
        cmds.setAttr (poci+".parameter", 1.0/(jntNum-1)*index )
        cmds.connectAttr (curveShape+'.worldSpace[0]', poci+'.inputCurve')
        cmds.connectAttr (poci+'.position', jointName[index]+'.translate')
        if not index==0:
            cmds.aimConstraint( jointName[index-1], jointName[index], aim=[-1, 0, 0], u=[0, 0, 1], wu=[0, 0, 1], wut='objectrotation', wuo= jointName[index-1] )
    
    loc = cmds.spaceLocator()[0]
    cmds.parent(loc, jointName[1])
    for attr in ['tx', 'ty', 'tz']:    cmds.setAttr (loc+'.'+attr, 0 )
    cmds.setAttr (loc+'.tz', cmds.arclen(curveName)/(jntNum-1))
    cmds.parent(loc, w=True)
    cmds.aimConstraint( jointName[1], jointName[0], aim=[1, 0, 0], u=[0, 0, 1], wu=[0, 0, 1], wut='object', wuo= loc )
    


def doDynRope (divNum):

    if divNum==0:
        divNum = cmds.intSliderGrp('num_ISG',q=True,  value=True )   #   rebuild Curve
        pfx = cmds.textFieldGrp('pfx_TFG',q=True, text=True  )
    inpCurv = cmds.ls(sl=True)[0]
    cmds.rebuildCurve(inpCurv, rt=0, d=3)
    cmds.rebuildCurve(inpCurv, rt=0, s=divNum)
    
    cmds.select (inpCurv)
    mm.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')
    crvShape= cmds.listRelatives (inpCurv, s=True)[0]
    folicle = cmds.listConnections (crvShape+".local") [0]
    folShape = cmds.listRelatives (folicle, s=True)[0]
    dynCurveShape = cmds.connectionInfo (folShape+".outCurve", destinationFromSource=True)[0].split('.')[0]   
    dynCurve = cmds.listRelatives (dynCurveShape, p=True)[0]		 
    hairSysShape = cmds.connectionInfo (folShape+".outHair", destinationFromSource=True)[0].split('.')[0] 
    hairSys = cmds.listRelatives (hairSysShape, p=True)[0] 
    
    cmds.group(hairSys,  cmds.listRelatives (folicle, p=True)[0],  cmds.listRelatives (dynCurve, p=True)[0], n=pfx+'Dyn_grp' )
    cmds.setAttr (hairSys+".visibility", 0)
    
    an_jntOnCurvNonspline (dynCurve, jntNum = divNum,   pfx=pfx,  geo=True)
    
    return dynCurve, folicle, hairSysShape
    






 











