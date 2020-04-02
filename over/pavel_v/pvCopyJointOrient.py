import maya.cmds as cmds
import maya.OpenMaya as om

def pvCopyJointOrient(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified couple of joints.')
        return
    if len(args) != 2:
        om.MGlobal.displayWarning('Must be specified only two joints.')
        return

    source, destination = args
    joint_orient = cmds.joint(source, query=True, orientation=True)
    cmds.joint(destination, edit=True, orientation=joint_orient)

# pvCopyJointOrient()