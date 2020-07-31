
from  an_Procedures.utilities import  an_convertSliceToList
import maya.cmds as cmds

 
def an_alignByFace( ):
    
    sel = an_convertSliceToList(cmds.ls(sl=True))
    if len(sel)==2:
        a_face, targetGeo =  sel
        geo = a_face.split('.')[0]
        verts = an_convertSliceToList(cmds.polyListComponentConversion(a_face, toVertex=True )) [:3]
        t_vetr = [ x.replace(geo, targetGeo) for x in verts ]
        
    elif len(sel)==6:
        targetGeo = sel[-1].split('.')[0]
        geo = sel[0].split('.')[0]
        verts = sel [:3]
        t_vetr = sel [3:]
        
    else: cmds.error( 'First select 3 vertices, then 3 vertices of the target geometry')
        
    locList=[]
    for ver in verts:
        coord = cmds.xform(ver, q=True, t=True, ws=True)    
        locList.append(cmds.spaceLocator( )[0])
        cmds.move (coord[0], coord[1], coord[2] )
        
    cmds.aimConstraint (locList[:2], worldUpType= 'object', worldUpObject = locList[2] )   
    constr = cmds.parentConstraint (locList[1], geo, mo=True  ) 
    
    for i in range(3):
        coord = cmds.xform(t_vetr[i] , q=True, t=True, ws=True)
        cmds.select(locList[i])
        cmds.move ( coord[0], coord[1], coord[2] )
        
    cmds.delete(constr, locList)