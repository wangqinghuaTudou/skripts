import maya.cmds as cmds
import maya.api.OpenMaya as om

def pvShowOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 1)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 0)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) shown successful.')

def pvHideOrigGeo(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified some object(s).')
        return

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            origShapes = shapes[1:]
            if origShapes:
                cmds.setAttr(shapes[0] + '.intermediateObject', 0)
                cmds.setAttr(origShapes[-1] + '.intermediateObject', 1)
            else:
                om.MGlobal.displayInfo('Object "%s" has no Original shapes.'%obj)
                continue
        else:
            om.MGlobal.displayInfo('Object "%s" has no any shapes.'%obj)
    om.MGlobal.displayInfo('Original shapes for specified object(s) hided successful.')

def pvDeleteOrigShapes(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified some object(s).')
        return

    deleted_shapes_counter = 0
    deletedShapes = []

    for obj in args:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
        if shapes:
            for shp in shapes:
                isOrig = cmds.getAttr (shp + '.intermediateObject')
                if isOrig:
                    isConnected = cmds.listConnections(shp, source=True, destination=True)
                    if not isConnected:
                        try:
                            deletedShapes.append(shp)
                            cmds.delete(shp)
                            deleted_shapes_counter += 1
                        except:
                            om.MGlobal.displayInfo('Can\'t delete "Orig" shape: ' + shp)

    if deletedShapes:
        om.MGlobal.displayInfo('-------------------------------------------------------------')
        om.MGlobal.displayInfo('Deleted %s shapes.'%deleted_shapes_counter)
        om.MGlobal.displayInfo('Deleted shapes:')
        om.MGlobal.displayInfo('%s'%deletedShapes)
    else:
        om.MGlobal.displayInfo('No "Orig" shapes deleted.')

    return deletedShapes

def pvCopyUV(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified two objects.')
        return
    if len(args) != 2:
        om.MGlobal.displayInfo('Must be specified only two objects.')
        return

    sample_space = pvCopyUVInterfaceRequest()
    source = args[0]
    dest = args[1]
    pvDeleteOrigShapes(source)
    pvDeleteOrigShapes(dest)
    pvShowOrigGeo(dest)

    cmds.transferAttributes(source, dest, \
                            transferPositions=0, \
                            transferNormals=0, \
                            transferUVs=2, \
                            transferColors=0, \
                            sampleSpace=sample_space, \
                            sourceUvSpace='map1', \
                            targetUvSpace='map1', \
                            searchMethod=3, \
                            flipUVs=0,
                            colorBorders=1)

    cmds.delete(dest, constructionHistory=True)
    pvHideOrigGeo(dest)
    cmds.select(dest, replace=True)
    om.MGlobal.displayInfo('Mapping replaced successfuly.')

def pvCopyUV_ui():

    sampleSpaceList = ['World', \
                       'Local', \
                       'UV', \
                       'Component', \
                       'Topology']

    if (cmds.window('pvCopyUV_ui', exists=True)):
        cmds.deleteUI('pvCopyUV_ui')

    cmds.window('pvCopyUV_ui', \
                resizeToFitChildren=True, \
                sizeable=False, \
                title='Copy UV')

    cmds.columnLayout ('pvMainLayoutCopyUV', \
                     width=300, \
                     height=170, \
                     adjustableColumn=True)

    cmds.text('pvTextSampleSpace', label='Sample Space:', align='right')

    cmds.optionMenuGrp('pvOptMenuGrpSampleSpace', columnWidth=[1, 80])
    for item in sampleSpaceList:
        cmds.menuItem(label=item)
    cmds.optionMenuGrp('pvOptMenuGrpSampleSpace', edit=True, select=4)

    cmds.button(label='Run', command='pvCopyUV()')
    
    cmds.showWindow('pvCopyUV_ui')

def pvCopyUVInterfaceRequest():

    win = 'pvCopyUV_ui'

    if not cmds.window(win, exists=True):
        om.MGlobal.displayInfo('Interface doesn\'t exists. Assigned default settings.')
        sample_space = 4
    else:
        if cmds.optionMenuGrp('pvOptMenuGrpSampleSpace', exists=True):
            sample_space = cmds.optionMenuGrp('pvOptMenuGrpSampleSpace', query=True, select=True)
            if sample_space < 3:
                sample_space -= 1
            om.MGlobal.displayInfo('Sample Space: %s'%sample_space)
        else:
            om.MGlobal.displayInfo('Interface doesn\'t exists. Assigned default settings.')
            sample_space = 4

    return sample_space

# pvCopyUV_ui()