import maya.cmds as cmds

def an_openHidedChannell():
    v_allObj = cmds.ls (sl=True )
    for v_Obj in v_allObj:
        for v_attr in ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v' ]:
            cmds.setAttr (v_Obj+v_attr, k=True,  lock=False )
            #cmds.setAttr (v_Obj+v_attr, k=True )
