import maya.cmds as cmds
import maya.OpenMaya as om

def pvBlendshapeSplitAxis():

    if (cmds.window('pvBlendshapeSplitAxis_ui', exists=True)):
        cmds.deleteUI('pvBlendshapeSplitAxis_ui')

    cmds.window('pvBlendshapeSplitAxis_ui', \
                resizeToFitChildren=True, \
                sizeable=False, \
                title='Split shape by axises.')

    cmds.columnLayout(adjustableColumn=True)
    cmds.text('Sel base, target shps.', align='center')
    cmds.separator (height=5, style='out')

    cmds.checkBox('pvBlendshapeSplitX_chbox', value=1, label='X', align='left')
    cmds.checkBox('pvBlendshapeSplitY_chbox', value=1, label='Y', align='left')
    cmds.checkBox('pvBlendshapeSplitZ_chbox', value=1, label='Z', align='left')
    cmds.separator(height=5, style='in')

    cmds.button(label='Run', command='pvBlendshapeSplitAxisMain()')
    
    cmds.showWindow('pvBlendshapeSplitAxis_ui')

def pvBlendshapeSplitAxisInterfaceRequest():

    win = 'pvBlendshapeSplitAxis_ui'

    if not cmds.window(win, exists=True):
        axis_list = ['x' ,'y', 'z']
    else:
        axis_list = []
        if cmds.checkBox('pvBlendshapeSplitX_chbox', query=True, value=True):
            axis_list.append('x')
        if cmds.checkBox('pvBlendshapeSplitY_chbox', query=True, value=True):
            axis_list.append('y')
        if cmds.checkBox('pvBlendshapeSplitZ_chbox', query=True, value=True):
            axis_list.append('z')

    return axis_list


def pvBlendshapeSplitAxisMain(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayInfo('Must be specified two object(s).')
        return
    if len(args) != 2: # check the count of selected objects
        om.MGlobal.displayWarning('Must be specified only two objects.')
        return

    axis_list = pvBlendshapeSplitAxisInterfaceRequest()
    if not axis_list:
        om.MGlobal.displayWarning('Must be specified at least one axis.')
        return
    base_shape, target_shape = args
    vertex_number = cmds.polyEvaluate(base_shape, vertex=True)
    for axs in axis_list:
        dup_name = cmds.duplicate(base_shape, name='%s_dup_%s'%(base_shape, axs))[0]

        bBox_base = cmds.polyEvaluate(boundingBox=True)
        if axs == 'x':
            bBox_x = bBox_base[0][1] - bBox_base[0][0]
            cmds.move(bBox_x * 1.1, 0, 0, dup_name, relative=True)
        if axs == 'y':
            bBox_y = bBox_base[1][1] - bBox_base[1][0]
            cmds.move(0, bBox_y * 1.1, 0, dup_name, relative=True)
        if axs == 'z':
            bBox_z = bBox_base[2][1] - bBox_base[2][0]
            cmds.move(0, 0, bBox_z * 1.1, dup_name, relative=True)

        for i in xrange(vertex_number):
            xform_vtx_base = cmds.xform('%s.vtx[%s]'%(base_shape, i), query=True, translation=True)
            xform_vtx_target = cmds.xform('%s.vtx[%s]'%(target_shape, i), query=True, translation=True)
            if axs == 'x':
                cmds.xform('%s.vtx[%s]'%(dup_name, i), translation=[xform_vtx_target[0], xform_vtx_base[1], xform_vtx_base[2]])
            if axs == 'y':
                cmds.xform('%s.vtx[%s]'%(dup_name, i), translation=[xform_vtx_base[0], xform_vtx_target[1], xform_vtx_base[2]])
            if axs == 'z':
                cmds.xform('%s.vtx[%s]'%(dup_name, i), translation=[xform_vtx_base[0], xform_vtx_base[1], xform_vtx_target[2]])
    om.MGlobal.displayInfo('Axis splited successfuly for blendshape "%s".'%base_shape)

# pvBlendshapeSplitAxis()