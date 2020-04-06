import maya.cmds as cmds
import maya.mel as mm
from an_Procedures.joints import an_jntOnCurv


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