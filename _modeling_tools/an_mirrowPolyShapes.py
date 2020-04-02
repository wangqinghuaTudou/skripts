import maya.cmds as cmds
from  anProcedures import *

'''
mirrow selected vertex to other geomerty (by id number)

'''


def an_mirrowPolyShapes():

    sel = cmds.ls(sl=1)
    
    if len(sel)==2:
        srs, target = sel
        sourseShape = cmds.listRelatives(srs, s=True)[0]  # get curve shape
        targShape = cmds.listRelatives(target, s=True)[0]
        vPointsNum = cmds.polyEvaluate(sourseShape,  v=True )   # get points number
        for pn in xrange(vPointsNum):
            pos = cmds.xform(sourseShape + '.vtx[' + str(pn) + ']', q=True, t=True, ws=True)
            cmds.xform(targShape + '.vtx[' + str(pn) + ']', t=[pos[0] * -1, pos[1], pos[2]], ws=True)
    else:
        srs, target = an_convertPointsNames(sel[:-1]), sel[-1]  
        targShape = cmds.listRelatives(target, s=True)[0]
        for vert in srs:
            pos = cmds.xform(vert, q=True, t=True, ws=True)
            cmds.xform(target +'.'+vert.split('.')[1], t=[pos[0] * -1, pos[1], pos[2]], ws=True)
            print (target +'.'+vert.split('.')[1])
            