#!/usr/bin/env python
# -*- coding: utf-8 -*-

#script for mirroring selected verticies on a single object (for example two combined gloves). Select verticies on source and run the an_mirrorPolyVertices()
import maya.mel as mm
import maya.cmds as cmds
from  an_Procedures.utilities import an_convertSliceToList

def an_mirrorPolyVertices(): 
    pList = an_convertSliceToList(cmds.ls(sl=1))
    pfx = pList[0].split('[')[0]
    mm.eval('ConvertSelectionToShell;') 
    partPList = an_convertSliceToList(cmds.ls(sl=1))
    ofset=len(partPList)  if pfx+'[0]' in partPList else (len(partPList))*(-1)
        
    for point in pList:
        pos = cmds.xform( point , q=True, t=True, ws=True  )
        oposPoint= pfx+'['+str( int(point.split('[')[1].split(']')[0])+ofset)+']'   
        cmds.xform(oposPoint , t=[pos[0] * -1, pos[1], pos[2]], ws=True)
    cmds.select (pList)
            