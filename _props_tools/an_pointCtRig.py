"""Controller creates and places it in the place of the selected object"""

import maya.cmds as cmds
from An_Controllers import An_Controllers  as ctrl

def an_pointCtRig ():
    target = cmds.ls(sl=True)
    result = cmds.promptDialog( title='Point Controller rig', message='Enter controller name:', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
    if result == 'OK':
        name = cmds.promptDialog(query=True, text=True)

    	v_ct = ctrl(name+'_CT')
    	v_ct.makeController ( 'sphere', size=1, offset = [0, 0, 0], orient="Y")
    	v_ct.gropeCT()
    	jnt = cmds.joint (n= name +'_jnt')
    	#cmds.parent(jnt , v_ct.name )
        if target:
            pos = cmds.xform (target[0], q=True,  t=True, ws=True  )
            cmds.move( pos[0], pos[1], pos[2], v_ct.oriGrp, absolute=True )
    else: pass

