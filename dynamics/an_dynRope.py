
 

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

def doDynRope (divNum):

    if divNum==0:
        divNum = cmds.intSliderGrp('num_ISG',q=True,  value=True )   #   rebuild Curve
    inpCurv = cmds.ls(sl=True)[0]
    cmds.rebuildCurve(inpCurv, rt=0, d=3)
    cmds.rebuildCurve(inpCurv, rt=0, s=divNum)

    cmds.select (inpCurv)
    mm.eval("makeCurvesDynamicHairs 0 0 0;")
    crvShape= cmds.listRelatives (inpCurv, s=True)[0]
    folicle = cmds.listConnections (crvShape+".local") [0]
    folShape = cmds.listRelatives (folicle, s=True)[0]
    dynCurveShape = cmds.connectionInfo (folShape+".outCurve", destinationFromSource=True)[0].split('.')[0]   
    dynCurve = cmds.listRelatives (dynCurveShape, p=True)[0]		 
    hairSysShape = cmds.connectionInfo (folShape+".outHair", destinationFromSource=True)[0].split('.')[0] 
    hairSys = cmds.listRelatives (hairSysShape, p=True)[0] 

    cmds.group(hairSys,  cmds.listRelatives (folicle, p=True)[0],  cmds.listRelatives (dynCurve, p=True)[0] )
    cmds.setAttr (hairSys+".visibility", 0)
    return dynCurve, folicle, hairSysShape





 











