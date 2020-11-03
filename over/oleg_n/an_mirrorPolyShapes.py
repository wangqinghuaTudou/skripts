#script for mirroring shapes of the polygonal objects. First select source, then target and run the script.
import maya.cmds as cmds
from  an_Procedures.utilities import an_convertSliceToList


def  an_mirrorPolyShapes():
    
    
    sel = cmds.ls(sl=1)
    if len(sel)==2:
    
        srs, target = sel
        sourseShape = cmds.listRelatives(srs, s=True)[0]  # get curve shape
        targShape = cmds.listRelatives(target, s=True)[0]
        vPointsNum = cmds.polyEvaluate(sourseShape,  v=True )                    # get curve points number
        for pn in xrange(vPointsNum):
            pos = cmds.xform(sourseShape + '.vtx[' + str(pn) + ']', q=True, t=True, ws=True)
            cmds.xform(targShape + '.vtx[' + str(pn) + ']', t=[pos[0] * -1, pos[1], pos[2]], ws=True)
    else:
        srs, target = an_convertSliceToList(sel[:-1]), sel[-1]  
        targShape = cmds.listRelatives(target, s=True)[0]
        for vert in srs:
            
            pos = cmds.xform(vert, q=True, t=True, ws=True)
            cmds.xform(target +'.'+vert.split('.')[1], t=[pos[0] * -1, pos[1], pos[2]], ws=True)
            
            print (target +'.'+vert.split('.')[1])
        