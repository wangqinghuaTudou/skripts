import maya.cmds as cmds
import maya.api.OpenMaya as om
from pvShowOrigGeo import *
from pvDeleteOrigShapes import *

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

    mc.text('pvTextSampleSpace', label='Sample Space:', align='right')

    mc.optionMenuGrp('pvOptMenuGrpSampleSpace', columnWidth=[1, 80])
    for item in sampleSpaceList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('pvOptMenuGrpSampleSpace', edit=True, select=4)

    cmds.button(label='Run', command='pvCopyUV()')
    
    cmds.showWindow('pvCopyUV_ui')

def pvCopyUVInterfaceRequest():

    win = 'pvCopyUV_ui'

    if not mc.window(win, exists=True):
        om.MGlobal.displayInfo('Interface doesn\'t exists. Assigned default settings.')
        sample_space = 4
    else:
        if mc.optionMenuGrp('pvOptMenuGrpSampleSpace', exists=True):
            sample_space = mc.optionMenuGrp('pvOptMenuGrpSampleSpace', query=True, select=True)
            if sample_space < 3:
                sample_space -= 1
            om.MGlobal.displayInfo('Sample Space: %s'%sample_space)
        else:
            om.MGlobal.displayInfo('Interface doesn\'t exists. Assigned default settings.')
            sample_space = 4

    return sample_space

# pvCopyUV()