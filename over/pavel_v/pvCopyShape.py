import maya.OpenMaya as om
import maya.cmds as cmds

def pvCopyShape(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return
    if len(args) != 2: # check count of the selected objects
        om.MGlobal.displayInfo('Must be specified two objects.')
        return

    source, destination = args

    selection = om.MSelectionList()
    dagPathSource = om.MDagPath()
    dagPathDestination = om.MDagPath()
    vertPoints = om.MPointArray()

    selection.add(source)
    selection.add(destination)

    selection.getDagPath(0, dagPathSource)
    selection.getDagPath(1, dagPathDestination)

    mfnObjectSource = om.MFnMesh(dagPathSource)
    mfnObjectDestination = om.MFnMesh(dagPathDestination)

    mfnObjectSource.getPoints(vertPoints)
    mfnObjectDestination.setPoints(vertPoints)

# pvCopyShape()