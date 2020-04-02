import maya.cmds as cmds
from An_Controllers import An_Controllers  as An_Controllers

def an_showAllSelectedObj():
    for vObj in  cmds.ls(sl=True):
        if cmds.objExists(vObj+'.tx'):
            An_Controllers(vObj).showTransAttrs()
            cmds.setAttr (vObj+'.v', lock=False)
            if cmds.connectionInfo( vObj+'.v', isDestination=True):
                source = cmds.connectionInfo( vObj+'.v', sourceFromDestination=True)
                cmds.disconnectAttr (source, vObj+'.v',)
            cmds.setAttr (vObj+'.v', 1)
            cmds.setAttr (vObj+'.overrideVisibility', 1)

