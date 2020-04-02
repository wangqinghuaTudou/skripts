import maya.cmds as cmds
from An_Controllers import An_Controllers as ctrl
from anProcedures import an_jntOnCurv as an_jntOnCurv
from an_twistSegment import * 

def an_ropeRig_v2():

    v_win = "SplineIKRigUi"

    if cmds.window (v_win, exists=True):
        cmds.deleteUI (v_win)

    cmds.window(v_win, t="Rope Rig Tools v.2", w=450, h=100)
    cmds.columnLayout(adj=1)
    cmds.separator(st="none", h=10)
    cmds.text("    Creates a chain of bones that stretches along the curve. Please select curve!", align="left")
    cmds.separator(st="none", h=10)
    cmds.textFieldButtonGrp('TFBG_Prefix', label="Prefix: ", bl="Assign", bc="cmds.textFieldButtonGrp ('TFBG_Prefix', e=True, tx= cmds.ls(sl=True)[0])")
    cmds.textFieldButtonGrp('TFBG_General_CT', label="General_CT: ", bl="Assign", bc="cmds.textFieldButtonGrp ('TFBG_General_CT', e=True, tx= cmds.ls(sl=True)[0])")

    # increase max number of joints to 500
    cmds.intSliderGrp('ISG_1', field=1, minValue=3, maxValue=500, value=20, label=" Joints number: ")
    # increase max number of controllers to 40
    cmds.intSliderGrp('ISG_2', field=1, minValue=2, maxValue=40, value=3, label=" Controllers number: ")
    cmds.separator(st="none", h=3)
    cmds.checkBoxGrp('CBG', columnWidth2=[141, 165], numberOfCheckBoxes=1, label='Stretchable: ', v1=True)
    cmds.showWindow(v_win)
    cmds.separator(st="none", h=10)
    cmds.button(l="Make rope rig", c="an_doRopeRig()")


def placeObjOnCurve(v_curve, obj, pos):
    loc = cmds.spaceLocator()[0]
    poci = cmds.createNode('pointOnCurveInfo')
    cmds.connectAttr(v_curve + '.worldSpace[0]', poci + '.inputCurve', force=True)
    cmds.setAttr(poci + '.parameter', pos)
    cmds.setAttr(poci + '.turnOnPercentage', 1)
    cmds.connectAttr(poci + '.position', loc + '.translate', force=True)
    locPos = cmds.duplicate(loc)[0]
    cord = cmds.getAttr( loc+'.translate')[0] 
    cmds.setAttr(locPos+'.translate', cord[0], cord[1], cord[2])
    aimVec = 1 if not pos==1 else -1
    cmds.setAttr(poci + '.parameter', pos+(0.01*aimVec))
    cmds.delete(cmds.aimConstraint(loc, locPos,  aim = [aimVec, 0, 0],       mo=False))     
    cmds.delete(cmds.parentConstraint( locPos, obj, mo=False))
    cmds.disconnectAttr(poci + '.position', loc + '.translate')
    cmds.delete(poci, loc, locPos)



def an_doRopeRig():
    
    newTape = True
    v_ctNumber = cmds.intSliderGrp('ISG_2', q=True, v=True)
    v_jntNum = cmds.intSliderGrp('ISG_1', q=True, v=True)
    v_prefix = cmds.textFieldButtonGrp('TFBG_Prefix', q=True, tx=True )
    v_general_CT = cmds.textFieldButtonGrp('TFBG_General_CT', q=True, tx=True )
    # check if number of cv(+2) not equal number of controllers then rebuild curve else don't rebuild
    # start
    v_curve = cmds.ls(selection=True)[0]
    v_curveShape = cmds.listRelatives(v_curve, shapes=True)[0]
    v_degree = cmds.getAttr(v_curveShape + '.degree')
    v_spans = cmds.getAttr(v_curveShape + '.spans')
    v_cvNumber = v_degree + v_spans
        
    if v_cvNumber != v_ctNumber + 2:
        # end
        v_curveName = cmds.rebuildCurve(v_curve, ch=0, rpo=1,  rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=v_ctNumber, d=3, tol=0.01)[0]
    else:
        v_curveName = v_curve
    cmds.setAttr(v_curveName + ".inheritsTransform", 0)
    
    v_CT_jntsName, v_CT_orisName = [], []
    for i in xrange(v_ctNumber):
        v_ct = ctrl(v_prefix + str(i) + '_CT')
        v_ct.makeController('sphere', size=1, offset=[0, 0, 0], orient="Y")
        #v_ct.gropeCT()
        v_ctJnt= cmds.joint(r=True, n=v_prefix + 'Ctrl' + str(i) + "_jnt_")
        cmds.parent(v_ctJnt, v_ct.name)
        v_CT_jntsName.append(v_ctJnt)
        v_CT_orisName.append(v_ct.oriGrp)
        # replace v_curve by v_curveShape because of new procedure
        placeObjOnCurve(v_curveShape, v_ct.oriGrp, 1.0 / (v_ctNumber - 1) * i)
    
    cmds.skinCluster(v_curveName, v_CT_jntsName, dr=4.5)
    v_Grp = cmds.group(v_CT_orisName, v_curveName , n=v_prefix + "_RigGrp" )

     
    if newTape:  
        skinJnt = an_jntOnCurv(v_curveName, jntNum=v_jntNum, stretchable=True, pfx=v_prefix)
        cmds.parent(skinJnt[0][0], skinJnt[1][0], v_Grp)
        cmds.parent(v_Grp, v_general_CT)
        cmds.connectAttr( v_general_CT+'.scaleX', v_curveName + '.scaleCompensator')    
    
    else: #use twist Segment 
        info={}
        info['pfx']=v_prefix
        info['curveName']=v_curveName
        info['jntNum'] = v_jntNum
        info['stretchable']=True
        info['twSettings'] =[(v_CT_jntsName[0], 'z'), (v_CT_jntsName[-1], 'z')] # define up vector
        info['scaleObj']= v_general_CT
        info['geo']=False
        info['subAx'] = 12
        info = an_twistSegment (info)
        return info

    
    

    
    

 
    
    