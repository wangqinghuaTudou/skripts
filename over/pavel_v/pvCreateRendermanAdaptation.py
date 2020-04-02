import maya.mel as mel
import sys
sys.path.append('//dataServer/Project/backup_s3d/lib/setup/maya/maya_scripts_rfm3/rigging_tools/over/pavel_v/')
from pvSetRenderAttributes import *

def pvCreateRendermanAdaptation():

    geo_grp = ''
    geo_middle = ''
    if cmds.objExists('geometry_grp'):
        geo_grp = 'geometry_grp'
        mesh_list = cmds.listRelatives(geo_grp, allDescendents=True, type='mesh')
        if mesh_list:
            pvSetRenderAttributes(mesh_list)
    if cmds.objExists('geo_normal'):
        geo_middle = 'geo_normal'
        mesh_list = cmds.listRelatives(geo_middle, allDescendents=True, type='mesh')
        if mesh_list:
            pvSetRenderAttributes(mesh_list)
    if cmds.objExists('geo_middle'):
        geo_middle = 'geo_middle'
        mesh_list = cmds.listRelatives(geo_middle, allDescendents=True, type='mesh')
        if mesh_list:
            pvSetRenderAttributes(mesh_list)

    sg_list = cmds.ls(type='shadingEngine')
    if not sg_list:
        print('Can not find any "Shading Engine" node.'),
    else:
        for sg in sg_list:
            mel.eval('rmanExecAEMenuCmd("%s", "Add Adaptation")'%sg)
            rman_adapt = cmds.listConnections(sg + '.rmanAdaptations[0]', source=True, destination=False)
            if rman_adapt:
                rman_adapt = rman_adapt[0]
                rmsgp_shdr = sg + '_rmsgp_shdr'
                rmsgp_shdr = cmds.shadingNode('RMSGPSurface', asShader=True, name=rmsgp_shdr)
                cmds.setAttr(rman_adapt + '.rman__torattr___adaptorMatchString', 'Reyes', type='string')
                cmds.connectAttr(rmsgp_shdr + '.message', '%s.rman__torattr___customShadingGroup'%rman_adapt, force=True)
                mel.eval('rmanSetAttr("%s", "rman__torattr___adaptorController", "$user:renderer");'%sg)
                curr_shdr = cmds.listConnections(sg + '.surfaceShader', source=True, destination=False)
                if curr_shdr:
                    color_tex = cmds.listConnections(curr_shdr[0] + '.color', source=True, destination=False)
                    if color_tex:
                        cmds.connectAttr(color_tex[0], rmsgp_shdr + '.surfaceColor', force=True)

#pvCreateRendermanAdaptation()