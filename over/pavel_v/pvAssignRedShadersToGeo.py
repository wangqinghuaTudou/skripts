import maya.cmds as cmds
import maya.OpenMaya as om

def pvAssignRedShadersToGeo():

    sg_list = cmds.ls(type='shadingEngine')
    if not sg_list:
        om.MGlobal.displayWarning('Info: Can\'t find any "Shading Engine" node.'),
    else:
        for sg in sg_list:
            if not cmds.objExists(sg + '.rsSurfaceShader'):
                om.MGlobal.displayInfo('Info: "rsSurfaceShader" attribute on shading group "%s" doesn\'t exists.'%sg)
            else:
                rs_shader_conn = cmds.listConnections(sg + '.rsSurfaceShader', source=True, destination=False)
                isRsExists = False
                if rs_shader_conn:
                    if 'RedshiftMaterial' in cmds.nodeType(rs_shader_conn[0]):
                        rs_shader = rs_shader_conn[0]
                        isRsExists = True
                if not isRsExists:
                    om.MGlobal.displayInfo('Info: Shading engine "%s" hasn\'t Redshift material connected.'%sg)
                else:
                    rs_shader_conn_attr = cmds.listConnections(sg + '.rsSurfaceShader', source=True, destination=False, plugs=True)
                    cmds.disconnectAttr(rs_shader_conn_attr[0], sg + '.rsSurfaceShader')
                    rs_shader_sg = rs_shader + '_REDSG'
                    rs_shader_sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=rs_shader_sg)
                    cmds.connectAttr(rs_shader + '.outColor', rs_shader_sg + '.surfaceShader')
                    cmds.select(clear=True)
                    cmds.hyperShade(objects=sg)
                    cmds.sets(edit=True, forceElement=rs_shader_sg)
                    om.MGlobal.displayInfo('Info: Redshift shader "%s" successfuly assigned to corresponding geometries.'%sg)

    cmds.select(clear=True)
    om.MGlobal.displayInfo('Info: All Redshift shaders successfuly assigned to corresponding geometries.')
    return True

# pvAssignRedShadersToGeo()