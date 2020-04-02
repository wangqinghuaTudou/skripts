import maya.cmds as cmds
import maya.OpenMaya as om

def pvCreateShaderFX(*args):

    create_gamma = False
    all_connections = True
    linear_space = True
    old_shader_delete = False
    old_shaders_list = []
    shaderFX_graph_file = '//cacheServer/Project/lib/remoteExecution/lib/setup/maya/shaderFxBase5.sfx'
    attributes_list = ['.coverage', \
                       '.translateFrame', \
                       '.rotateFrame', \
                       '.mirrorU', \
                       '.mirrorV', \
                       '.stagger', \
                       '.wrapU', \
                       '.wrapV', \
                       '.repeatUV', \
                       '.offset', \
                       '.rotateUV', \
                       '.noiseUV' , \
                       '.vertexUvOne', \
                       '.vertexUvTwo', \
                       '.vertexUvThree', \
                       '.vertexCameraOne']

    if not cmds.pluginInfo('shaderFXPlugin', query=True, loaded=True):
        try:
            cmds.loadPlugin('shaderFXPlugin')
        except Exception, err:
            om.MGlobal.displayWarning(err)
            om.MGlobal.displayInfo('"shaderFXPlugin" Can\'t be loaded.')
            return

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        blin_list = ['animBlin_shdr']
        blinTexGamma_list = ['animBlinTex_gamma']
        blinTexFile_list = ['animBlinTex_file']
        place2dTex_list = ['animPlace_2dTex']
        shaderFX_list = ['animShaderFX_shdr']
        is_multiply_list = False
    else:
        blin_list = []
        blinTexGamma_list = []
        blinTexFile_list = []
        place2dTex_list = []
        shaderFX_list = []
        for obj in args:
            if '_obj' in obj:
                obj = obj.replace('_obj', 'Obj')
            if '|' in obj:
                obj = obj.split('|')[-1]
            blin_list.append(obj + 'Blin_shdr')
            blinTexGamma_list.append(obj + 'BlinTex_gamma')
            blinTexFile_list.append(obj + 'BlinTex_file')
            place2dTex_list.append(obj + 'Place_2dTex')
            shaderFX_list.append(obj + 'ShaderFX_shdr')
        is_multiply_list = True

    for i, obj in enumerate(blin_list):
        blin_name = blin_list[i]
        blinTexGamma = blinTexGamma_list[i]
        blinTexFile = blinTexFile_list[i]
        place2dTex = place2dTex_list[i]
        shaderFX_name = shaderFX_list[i]
        sg_name = blin_name + 'SG'
        blin_name = cmds.shadingNode('blinn', asShader=True, name=blin_name)
        sg_name = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
        cmds.setAttr(blin_name + '.eccentricity', 0)
        cmds.setAttr(blin_name + '.specularColor', 0, 0, 0, type='double3')

        blinTexFile = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=blinTexFile)
        place2dTex = cmds.shadingNode('place2dTexture', asUtility=True, name=place2dTex)

        for attr in attributes_list:
            cmds.connectAttr(place2dTex + attr, blinTexFile + attr, force=True)
        cmds.connectAttr(place2dTex + '.outUV', blinTexFile + '.uv', force=True)
        cmds.connectAttr(place2dTex + '.outUvFilterSize', blinTexFile + '.uvFilterSize', force=True)

        if create_gamma:
            blinTexGamma = cmds.shadingNode('gammaCorrect', asUtility=True, name=blinTexGamma)
            cmds.connectAttr(blinTexFile + '.outColor', blinTexGamma + '.value')
            cmds.connectAttr(blinTexGamma + '.outValue', blin_name + '.color')
            cmds.setAttr(blinTexGamma + '.gammaX', 2.2)
            cmds.setAttr(blinTexGamma + '.gammaY', 2.2)
            cmds.setAttr(blinTexGamma + '.gammaZ', 2.2)
        else:
            cmds.connectAttr(blinTexFile + '.outColor', blin_name + '.color')

        shaderFX_name = cmds.shadingNode('ShaderfxShader', asShader=True, name=shaderFX_name)
        cmds.connectAttr(shaderFX_name + '.outColor', blin_name + '.hardwareShader', force=True)
        cmds.shaderfx(sfxnode=shaderFX_name, loadGraph=shaderFX_graph_file)
        cmds.shaderfx(sfxnode=shaderFX_name, edit_bool=[1325, 'value', True])
        if linear_space:
            cmds.shaderfx(sfxnode=shaderFX_name, edit_bool=[1264, 'value_ConvertToLinearSpace', True])

        if is_multiply_list:
            obj_shape_list = cmds.listRelatives(obj, shapes=True, fullPath=True)
            if not obj_shape_list:
                om.MGlobal.displayInfo('Object "%s" hasn\'t any shapes.'%obj)
            else:
                obj_shape = obj_shape_list[0]
                sg_list = cmds.listConnections(obj_shape, source=False, destination=True, type='shadingEngine')
                if sg_list:
                    sg_list = list(set(sg_list))
                    current_sg = sg_list[0]
                    old_shaders_list.append(current_sg)
                    old_shaders_list += pvGetShadingNetwork(current_sg, [], 0)

                    file_node = pvFindFileNode(current_sg)
                    if file_node:
                        texture_path = cmds.getAttr(file_node + '.fileTextureName')
                        if texture_path:
                            texture_path_parts = texture_path.split('\\')
                            if len(texture_path_parts) < 2:
                                texture_path_parts = texture_path.split('/')
                            texture_name = texture_path_parts[-1]
                            character_name = texture_path_parts[7]
                            dds_textures_path = '//dataServer/Project/UrfinJuse2/assets/chars/%s/textures/color/cached/'%character_name
                            dds_texture = texture_name[:-4]
                            dds_texture = dds_texture + '.dds'
                            current_dds_textures_path = dds_textures_path + dds_texture
                            cmds.shaderfx(sfxnode=shaderFX_name, edit_stringPath=[1264, 'texturepath_MyTexture', current_dds_textures_path])
                            cmds.setAttr(blinTexFile + '.fileTextureName', current_dds_textures_path, type='string')

                    cmds.connectAttr(blin_name + '.outColor', sg_name + '.surfaceShader', force=True)
                    if all_connections:
                        sg_meshes_list = cmds.listConnections(current_sg, source=True, destination=False, type='mesh', skipConversionNodes=True)
                    else:
                        sg_meshes_list = [obj_shape]
                    if sg_meshes_list:
                        for i, sgm in enumerate(sg_meshes_list):
                            cmds.select(sgm, replace=True)
                            cmds.sets(edit=True, forceElement=sg_name)
                            #cmds.connectAttr(sgm + '.instObjGroups', sg_name + '.dagSetMembers[%s]'%i, force=True)

                    old_shaders_list.append(current_sg)

    if old_shaders_list and old_shader_delete:
        cmds.delete(old_shaders_list)

    om.MGlobal.displayInfo('-------------------------------------------------------------')
    om.MGlobal.displayInfo(blin_list)
    om.MGlobal.displayInfo(shaderFX_list)
    om.MGlobal.displayInfo('Viewport "blin" shader(s) with "shaderFX" created successful.')

    cmds.select(clear=True)

    return blin_list, shaderFX_list

'''
def pvIsShaderFx(current_sg):
    is_shaderfx = False
    blin_shader = cmds.listConnections(current_sg + '.surfaceShader', source=True, destination=False)
    if blin_shader:
        shader_fx = cmds.listConnections(blin_shader[0] + '.hardwareShader', source=True, destination=False)
        if shader_fx:
            if cmds.objectType(shader_fx[0], isType='ShaderfxShader'):
                is_shaderfx = True
    return is_shaderfx
'''

def pvFindFileNode(node):
    file_name = ''
    conn_nodes_list = cmds.listConnections(node, source=True, destination=False, skipConversionNodes=True)
    if not conn_nodes_list:
        return file_name
    else:
        file_list = cmds.ls(conn_nodes_list, type='file')
        if file_list:
            file_name = file_list[0]
            return file_name
        else:
            for conn in conn_nodes_list:
                file_name = pvFindFileNode(conn)
                return file_name

def pvGetShadingNetwork(node, shading_network, iterations):
    conn_nodes_list = cmds.listConnections(node, source=True, destination=False, skipConversionNodes=True)
    if not conn_nodes_list:
        return shading_network
    else:
        for conn in conn_nodes_list:
            conn_type = cmds.objectType(conn)
            if conn in shading_network or conn_type == 'mesh' or conn_type == 'nurbsCurve' or conn_type == 'nurbsSurface':
                return shading_network
            else:
                shading_network.append(conn)
                shading_network = pvGetShadingNetwork(conn, shading_network, iterations + 1)
                return shading_network

pvCreateShaderFX()