

import maya.cmds as cmds
import maya.mel as mm

def an_trackCreater ():
    win = "an_trackCreater"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Track creation system. v01", rtf=True ,menuBar=True )
    cmds.menu (label="Edit" )
    cmds.menuItem (label='Load "l_track" preset', command="cmds.textFieldGrp ('pfxTFG', e=True, tx='l_track')")
    cmds.menuItem (label='Load "r_track" preset', command="cmds.textFieldGrp ('pfxTFG', e=True, tx='r_track')")
    cmds.menu (label="Help" )
    vCLayout =cmds.columnLayout()
    cmds.frameLayout (label="Track rigging system", cll=1, w=445) ###, borderStyle="etchedIn"
    cmds.columnLayout
    cmds.textFieldGrp('pfxTFG', label='Prefix:', columnWidth2 = [220, 171 ]  )
    cmds.radioButtonGrp('plane_RBG', label='Constructive plane:', labelArray3=['YZ', 'YX', 'ZX'], numberOfRadioButtons=3, columnWidth4 = [220, 90, 90, 90], sl=1)
    cmds.textFieldButtonGrp('curve_TFBG', label='Path curve:', buttonLabel='Button', columnWidth3=[220, 171, 100], bl='   Add  ', bc="cmds.textFieldButtonGrp ('curve_TFBG', e=True, tx= cmds.ls(sl = True)[0])" )
    cmds.intSliderGrp('curve_ISG', field=True, label='Quality:', columnWidth3=[220, 50, 165], v=50 )
    cmds.intSliderGrp('track_ISG', field=True, label='Number of track elements:', columnWidth3=[220, 50, 165], v=20, max=200  )
    cmds.rowColumnLayout ( numberOfColumns=4, columnWidth=[ (1, 5  ), (2, 212), (3, 5  ), (4, 212)])
    cmds.text (l="", align="right")
    cmds.button (label="Delete rigging system", c= "an_delRig (cmds.ls(sl=True)[0])")
    cmds.text (l="", align="right")
    cmds.button (label="Make track rigging system", c= "an_doRigSys()")
    cmds.separator(h=3, style='none' )
    cmds.setParent (vCLayout)
    cmds.separator(h=3, style='none' )
    cmds.frameLayout (label="Atach geometry to joint", cll=1, w=445)#, borderStyle="etchedIn"
    cmds.columnLayout
    cmds.separator(h=3, style='none' )
    cmds.radioButtonGrp('typy_RBG', label='Duplikate sourse us:', labelArray2=['Duplikate','Instans'   ], numberOfRadioButtons=2, columnWidth3 = [220, 90, 90 ], sl=1)
    cmds.intSliderGrp('step_ISG', field=True, label='Step:', columnWidth3=[220, 50, 165], v=1, min=1, max=5 )
    cmds.rowColumnLayout ( numberOfColumns=2, columnWidth=[ (1, 222), (2, 212)])
    cmds.text (l="", align="right")
    cmds.button (label="Atach", c= "an_attachGeoToPath()")
    cmds.showWindow (win)
#-------------------------------------------------

def an_attachGeoToPath():
    v_pfx = cmds.textFieldGrp ('pfxTFG', q=True, tx=True)
    v_geo = cmds.ls(sl = True)[0]
    v_jnt = an_childCapture(cmds.ls(sl = True)[1])
    v_grp = cmds.group (em=True, n=v_pfx+v_geo+'Geo_grp')

    for v_each in v_jnt[:-1:cmds.intSliderGrp('step_ISG', q=True,  v=True )]:
        if cmds.radioButtonGrp('typy_RBG', q=True, sl=True)==1:
            v_copy = cmds.duplicate( v_geo, n= v_pfx+v_geo)[0]
        else :
            v_copy = cmds.duplicate( v_geo, ilf= True, n= v_pfx+v_geo )[0]
        cmds.parentConstraint( v_each, v_copy )
        cmds.parent (v_copy, v_grp)
#-------------------------------------------------
def an_childCapture(v_root):
    v_jntList = [v_root]
    v_obj= v_jntList [0]
    while cmds.listRelatives (v_obj, children=True ):
        v_obj = cmds.listRelatives (v_obj, children=True )[0]
        v_jntList.append(v_obj)
    return v_jntList
#-------------------------------------------------
def an_stretchSplinIk(v_pfx, v_curve, v_jntNum):
    v_arcLength  = cmds.arclen (v_curve, ch=True)
    v_arcLength = cmds.rename(v_arcLength, v_pfx+v_arcLength  )
    v_jntLevgth = cmds.getAttr (v_arcLength+'.arcLength')/v_jntNum
    v_jointNames=[]
    v_MDVnod= cmds.shadingNode ('multiplyDivide', n= v_pfx+'MDV', asUtility=True)
    cmds.setAttr (v_MDVnod+".operation", 2)
    cmds.connectAttr (v_arcLength+".arcLength",  v_MDVnod+".input1X")
    cmds.setAttr (v_MDVnod+".input2X", cmds.getAttr (v_arcLength+'.arcLength'))
    for v_I in xrange(0,v_jntNum):
        v_jnt = cmds.joint (r=True,  n=v_pfx+str(v_I)+'_jnt', p=[v_jntLevgth, 0, 0])
        v_jointNames.append(v_jnt)
        cmds.connectAttr (v_MDVnod+".outputX",  v_jnt+".sx")
    v_ikHandle = cmds.ikHandle (sol='ikSplineSolver', n= v_pfx+'ikHandle', ccv=False, pcv=False, sj=v_jointNames[0], c=v_curve)[0]
    an_delSys ([v_MDVnod, v_arcLength], v_ikHandle)
    return v_ikHandle, v_jointNames
#-------------------------------------------------
def an_connectRigVis (v_ct, v_obj):
    if not mm.eval( 'attributeExists "rigVis"'+v_ct): cmds.addAttr (v_ct, ln="rigVis",  dv=0, k=True, at="enum", en="off:on" )
    for v_each in v_obj:
        if  not cmds.connectionInfo (v_each+".v",id=True):
    	    cmds.connectAttr  (v_ct+".rigVis", v_each+".v")
#-------------------------------------------------
def an_delRig (v_Obg):
    if mm.eval( 'attributeExists "delList"'+v_Obg) and mm.eval('objExists '+v_Obg) :
        v_delObgList = str(cmds.getAttr  (v_Obg +".delList")).split("***")[:-1]
        print v_delObgList
        for v_iobj in v_delObgList:
            print v_iobj
            an_delRig (v_iobj)
        if mm.eval('objExists '+v_Obg): cmds.delete(v_Obg)
    else :
        if mm.eval('objExists '+v_Obg): cmds.delete(v_Obg)
#-------------------------------------------------
def an_delSys (v_objs, v_ct):
    if not mm.eval( 'attributeExists "delList"'+v_ct):
        cmds.addAttr (v_ct, ln="delList", k=False, dt="string"  )
    for v_each in v_objs:
        v_val = str(cmds.getAttr  (v_ct +".delList"))
        print v_val, v_each
        if  v_val=='None':  cmds.setAttr (v_ct+".delList", v_each+"***", type="string")
        else : cmds.setAttr (v_ct+".delList",  v_val+v_each+"***", type="string")
#-------------------------------------------------

def an_doRigSys ():

    pathCurve = cmds.textFieldButtonGrp ('curve_TFBG', q=True, tx=True) #get data
    v_pfx = cmds.textFieldGrp ('pfxTFG', q=True, tx=True)
    v_Quality = cmds.intSliderGrp('curve_ISG', q=True, v=True)
    v_trackNum = cmds.intSliderGrp('track_ISG', q=True, v=True)
    v_pl = cmds.radioButtonGrp('plane_RBG', q=True, sl=True)
    v_axis = [1,0,0] if  v_pl==1 else [0,0,1]
    if v_pl==3: v_axis = [0,1,0]

    cmds.rebuildCurve(pathCurve, rt=0, s=v_Quality, ch=True, d=1) #rebuild and made polyExtrude
    rotCurve = cmds.circle (nr=v_axis, n=v_pfx+"Curve", d=3, tol=0.01, s=10, ch=False)[0] # made circle, rebuild and made polyExtrude for wrap
    cmds.rebuildCurve(rotCurve, rt=0, s=v_Quality, ch=False, d=1)
    curveForBSh = cmds.duplicate (rotCurve, name= v_pfx+"CurveForBSh",   rr=True)[0]

    v_ct = cmds.spaceLocator (n=v_pfx+"Ctrl")[0] #making  controller
    cmds.addAttr (v_ct, ln='rotateTrack', dv=0, k= True)
    cmds.addAttr (v_ct, ln='jntSize', dv=0, k= True)

    v_rotChannel = '.rx' if  v_pl==1 else '.rz'
    if v_pl==3: v_rotChannel = '.ry'
    cmds.connectAttr (v_ct+'.rotateTrack', rotCurve+v_rotChannel)
    cmds.wire (rotCurve,  gw=False, en=1.000000, ce=0.000000, li=0.000000,  w=curveForBSh  )
    cmds.blendShape(pathCurve, curveForBSh, origin='world', tc=0, w=[(0, 1)])
    v_ikHandle, v_joints = an_stretchSplinIk (v_pfx, rotCurve, v_trackNum) #A making of Joints and stretch ik handle

    cmds.setAttr (v_ct+".jntSize",  cmds.getAttr (v_joints[-1]+'.tx') )
    for v_eachJnt in  v_joints[1:]:  cmds.connectAttr (v_ct+'.jntSize', v_eachJnt+'.tx')
    cmds.setAttr (v_ikHandle+".dTwistControlEnable",  1)
    cmds.setAttr (v_ikHandle+".dWorldUpType",  3)
    cmds.connectAttr (v_ct+'.worldMatrix[0]' , v_ikHandle+'.dWorldUpMatrix')
    for v_val, v_ax in zip (v_axis, ["X", "Y", "Z",]) : cmds.setAttr (v_ikHandle+".dWorldUpVector"+v_ax,  v_val)  #orient gnt

    v_Grp = cmds.group ( v_ikHandle, v_joints[0],  rotCurve, curveForBSh, curveForBSh+'BaseWire', v_ct,  n=v_pfx+'Rig_grp')
    an_delSys ([v_ikHandle, v_joints[0], rotCurve, curveForBSh, curveForBSh+'BaseWire',   v_ct,  rotCurve], v_Grp)
    an_connectRigVis (v_Grp, [v_ikHandle, rotCurve, curveForBSh])
    v_aim = cmds.aimConstraint( v_joints[0], v_joints[-1], aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType="objectrotation", worldUpVector=[0, 1, 0], worldUpObject=v_joints[0]  )  [0]













































