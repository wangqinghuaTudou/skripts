import maya.cmds as cmds
from an_Procedures.utilities import an_delSys

'''
        joints
-createBonesFromEdges ()           
-an_convertSliceToList()   
      
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
    

def an_jntOnCurv(curveName, jntNum = 10, stretchable=True, pfx=''):
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
    ikHandl = cmds.ikHandle  (n=pfx+'_ik', sol='ikSplineSolver',   ccv=False,  pcv=False,  sj=jointName[0], ee= jointName[-1], c=curveName)
    cmds.parent (jointName[0], curveName)
    if stretchable: an_delSys(ikHandl[0], objList =[jointName[0], jntPosMDVnod, scaleMDVnod, curvLength])
    else: an_delSys(ikHandl[0], objList =[jointName[0], ])
    return jointName, ikHandl