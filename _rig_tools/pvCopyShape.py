import maya.OpenMaya as om


def pvCopyShape(source, destination):

    selection = om.MSelectionList()
    dagPathSource = om.MDagPath()
    dagPathDestination = om.MDagPath()

    try:
        selection.add(source)
        selection.add(destination)
        selection.getDagPath(0, dagPathSource)
        selection.getDagPath(1, dagPathDestination)
    except: raise

    try:
        vertPoints = om.MPointArray()
        mfnObjectSource = om.MFnMesh(dagPathSource)
        mfnObjectDestination = om.MFnMesh(dagPathDestination)
        mfnObjectSource.getPoints(vertPoints)
        mfnObjectDestination.setPoints(vertPoints)
    except: raise


# pvCopyShape()