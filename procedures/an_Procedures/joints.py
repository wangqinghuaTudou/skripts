import maya.cmds as cmds
from an_Procedures.utilities import an_delSys

'''
        joints
-createBonesFromEdges ()           
-an_jntOnCurv() 
-jntOnCurvNonSpline()  
      
'''

def createBonesFromEdges (jntNum = 7):
    smuthnes = len(cmds.ls(sl=True))//3
    curv = mm.eval( 'polyToCurve -form 2 -degree 3;' )[0]
    cmds.delete(ch=True)
    cmds.rebuildCurve(curv, rt=0, s=smuthnes, constructionHistory=False )
    
    cmds.reverseCurve(curv,  constructionHistory=False )
    jntXval = cmds.arclen(curv)/jntNum
    res = an_jntOnCurv(curv, jntNum = jntNum, stretchable=False, pfx='')
    try:  cmds.parent(res[0][0], w=True)
    except RuntimeError :  pass
    cmds.delete(res[1], curv)
    cmds.makeIdentity (apply=True, t=1, r=1, s=1, n=0, pn=1)
   
    return res[0]
    
#an_jntOnCurv(curveName='curve1', jntNum = 50, stretchable=True, pfx='rp1',  geo=True)


def an_jntOnCurv(curveName, jntNum = 10, stretchable=True, pfx='', geo=False):
    pfx = curveName+'ChSys' if not pfx else pfx
    cmds.select (cl=True,  sym =True)
    if stretchable: #If the joints should be stretched.
        curvLength  = cmds.arclen(curveName, constructionHistory = stretchable )
        if not cmds.objExists(curveName+'.scaleCompensator'): cmds.addAttr (curveName, ln='scaleCompensator', k=True, dv=1)

        jntPosMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'jPosMDV',  asUtility=True)
        cmds.connectAttr (curvLength+'.arcLength',  jntPosMDVnod+'.input1X')
        cmds.setAttr (jntPosMDVnod+".input2X", jntNum)
        cmds.setAttr (jntPosMDVnod+".operation", 2)

        scaleMDVnod = cmds.shadingNode ('multiplyDivide', n=pfx+'scaleMDV',  asUtility=True)
        cmds.connectAttr (jntPosMDVnod+'.outputX',  scaleMDVnod+'.input1X')
        cmds.connectAttr (curveName+'.scaleCompensator',  scaleMDVnod+'.input2X')
        cmds.setAttr (scaleMDVnod+".operation", 2)
    jointName = range(jntNum+1)
    for index, string in enumerate(range(jntNum+1)):
    		 jointName[index]= cmds.joint (r=True , n=pfx+str(index)+'_jnt', p= [cmds.arclen(curveName)/jntNum, 0, 0])
    		 if stretchable: cmds.connectAttr (scaleMDVnod+'.outputX',  jointName[index]+'.tx')
    		 
    if geo:
        geo = cmds.polyCylinder( r=cmds.arclen(curveName)/jntNum/8, h=cmds.arclen(curveName),  sy= jntNum , sx=6, ax=[1, 0, 0])[0]
        cmds.delete(cmds.pointConstraint(jointName[0],jointName[-1], geo))
        cmds.skinCluster(jointName, geo, tsb=True, normalizeWeights=True)
	 
    ikHandl = cmds.ikHandle  (n=pfx+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=jointName[0], ee= jointName[-1], c=curveName)
    cmds.parent (jointName[0], curveName)
    if stretchable: an_delSys(ikHandl[0], objList =[jointName[0], jntPosMDVnod, scaleMDVnod, curvLength])
    else: an_delSys(ikHandl[0], objList =[jointName[0], ])
    return jointName, ikHandl
    
 
def jntOnCurvNonSpline(curve_name, jnt_num=10, pfx='', geo=True):
    
    pfx = curve_name + 'JntOnCurve' if not pfx else pfx
    curve_shape = cmds.listRelatives(curve_name, s=True)[0]
    jointsNames = range(jnt_num + 1)
    rigGrp = cmds.group(n=pfx + 'Joints_grp', em=True)
    jointsNames = range(jnt_num)
    curve_len = cmds.arclen(curve_name)
    
    cmds.select(cl=True, sym=True)
    for i, string in enumerate(range(jnt_num)):
        jointsNames[i] = cmds.joint(relative=True,
                                  name=pfx + str(i) + '_jnt',
                                  position=[curve_len / (jnt_num - 1), 0, 0])
    if geo:
        geo = cmds.polyCylinder(name=pfx + 'Skin_geo',
                                radius=curve_len / jnt_num / 8,
                                height=curve_len,
                                subdivisionsY=jnt_num - 1,
                                subdivisionsX=6,
                                axis=[1, 0, 0])[0]
        cmds.delete(cmds.pointConstraint(jointsNames[0], jointsNames[-1], geo))
        cmds.skinCluster(jointsNames, geo, tsb=True, normalizeWeights=True)
        cmds.parent(geo, rigGrp)

    for i, string in enumerate(range(jnt_num)):
        cmds.select(cl=True, sym=True)
        cmds.parent(jointsNames[i], rigGrp)
        point_on_curve_info = cmds.createNode('pointOnCurveInfo', n=pfx + str(i) + '_poci')
        cmds.setAttr(point_on_curve_info + ".turnOnPercentage", 1)
        cmds.setAttr(point_on_curve_info + ".parameter", 1.0 / (jnt_num - 1) * i)
        cmds.connectAttr(curve_shape + '.worldSpace[0]', point_on_curve_info + '.inputCurve')
        cmds.connectAttr(point_on_curve_info + '.position', jointsNames[i] + '.translate')
        if not i == 0:
            cmds.aimConstraint(jointsNames[i - 1], jointsNames[i],
                               aim=[-1, 0, 0],
                               upVector=[0, 0, 1],
                               worldUpVector=[0, 0, 1],
                               worldUpType='objectrotation',
                               worldUpObject=jointsNames[i - 1])
    loc = cmds.spaceLocator(name=pfx + 'Up_loc')[0]
    cmds.parent(loc, jointsNames[0])
    for attr in ['tx', 'ty', 'tz']:    cmds.setAttr(loc + '.' + attr, 0)
    cmds.setAttr(loc + '.tz', curve_len / (jnt_num - 1))
    cmds.parent(loc, w=True)
    cmds.aimConstraint(jointsNames[1], jointsNames[0],
                       aim=[1, 0, 0],
                       upVector=[0, 0, 1],
                       worldUpVector=[0, 0, 1],
                       worldUpType='object',
                       worldUpObject=loc)
    cmds.parent(loc, rigGrp)
    return loc, jointsNames, rigGrp







