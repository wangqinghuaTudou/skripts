import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import os
import re

def pvCreateTexture(texture_name='color', texture_path=''):

    tex_file = texture_name + 'Tex_file'
    tex_2d = texture_name + 'Tex_2d'
    tex_file = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=tex_file)
    tex_2d = cmds.shadingNode('place2dTexture', asUtility=True, name=tex_2d)
    cmds.connectAttr(tex_2d + '.coverage', tex_file + '.coverage', force=True)
    cmds.connectAttr(tex_2d + '.translateFrame', tex_file + '.translateFrame', force=True)
    cmds.connectAttr(tex_2d + '.rotateFrame', tex_file + '.rotateFrame', force=True)
    cmds.connectAttr(tex_2d + '.mirrorU', tex_file + '.mirrorU', force=True)
    cmds.connectAttr(tex_2d + '.mirrorV', tex_file + '.mirrorV', force=True)
    cmds.connectAttr(tex_2d + '.stagger', tex_file + '.stagger', force=True)
    cmds.connectAttr(tex_2d + '.wrapU', tex_file + '.wrapU', force=True)
    cmds.connectAttr(tex_2d + '.wrapV', tex_file + '.wrapV', force=True)
    cmds.connectAttr(tex_2d + '.repeatUV', tex_file + '.repeatUV', force=True)
    cmds.connectAttr(tex_2d + '.offset', tex_file + '.offset', force=True)
    cmds.connectAttr(tex_2d + '.rotateUV', tex_file + '.rotateUV', force=True)
    cmds.connectAttr(tex_2d + '.noiseUV', tex_file + '.noiseUV', force=True)
    cmds.connectAttr(tex_2d + '.vertexUvOne', tex_file + '.vertexUvOne', force=True)
    cmds.connectAttr(tex_2d + '.vertexUvTwo', tex_file + '.vertexUvTwo', force=True)
    cmds.connectAttr(tex_2d + '.vertexUvThree', tex_file + '.vertexUvThree', force=True)
    cmds.connectAttr(tex_2d + '.vertexCameraOne', tex_file + '.vertexCameraOne', force=True)
    cmds.connectAttr(tex_2d + '.outUV', tex_file + '.uv', force=True)
    cmds.connectAttr(tex_2d + '.outUvFilterSize', tex_file + '.uvFilterSize', force=True)
    cmds.setAttr(tex_file + '.fileTextureName', texture_path, type='string')
    return tex_file, tex_2d

def pvGetTexFilesList(color_file, texture_path):

    mapid_expression = re.compile( '_MAPID_|_u[0-9]+_v[0-9]+|_u\<u\>_v\<V\>|\<UDIM\>|[0-9][0-9][0-9][0-9]+', re.I )

    texture_directory = '/'.join(texture_path.split('/')[:-1])
    texture_name = texture_path.split('/')[-1]

    searched = mapid_expression.search( texture_name )

    if searched:
        texture_name_b = texture_name[:searched.start( 0 )]
        texture_name_e = texture_name[searched.end( 0 ):]
        texture_suffix = searched.group()

    texture_directory_cache = {}
    texture_queue = []
    directory_entry_list = []
    if texture_directory !='':
        if texture_directory not in texture_directory_cache:
            try:
                directory_entry_list = os.listdir( texture_directory )
            except Exception, err:
                om.MGlobal.displayError('Info: Texture path in node "%s" is inocorrect.'%color_file)
                om.MGlobal.displayError('Info: %s'%texture_directory)
            if directory_entry_list:
                for t in xrange( len( directory_entry_list ) -1, -1, -1 ):
                    if not directory_entry_list[t].count( '.' ):
                        directory_entry_list.pop( t )
                        continue
                texture_directory_cache[texture_directory] = directory_entry_list
        else:
            directory_entry_list = texture_directory_cache[texture_directory]

        texture_candidate_list = []
        for texture_candidate in directory_entry_list:
            searched_second = mapid_expression.search( texture_candidate )
            if searched_second:
                texture_candidate_name_b = texture_candidate[:searched_second.start( 0 )]
                texture_candidate_name_e = texture_candidate[searched_second.end( 0 ):]
                texture_candidate_suffix = searched_second.group()
                if texture_candidate_name_b != texture_name_b:
                    continue
                if texture_candidate_name_e != texture_name_e:
                    continue
                texture_candidate_list.append( texture_directory + '/' + texture_candidate )
        if len( texture_candidate_list ) > len( texture_queue ):
            texture_queue = texture_candidate_list

    return texture_queue

def pvCreateBlinToRman():

    sg_list = cmds.ls(type='shadingEngine')
    if not sg_list:
        om.MGlobal.displayWarning('Info: Can not find any "Shading Engine" node.'),
    else:
        rman_adapt_shdrs_list = []
        for sg in sg_list:
            if not cmds.objExists(sg + '.message'):
                om.MGlobal.displayInfo('Info: "message" attribute on shading group "%s" doesn\'t exists.'%sg)
            else:
                sg_message_conn = cmds.listConnections(sg + '.message', source=False, destination=True)
                isAdaptExists = False
                if sg_message_conn:
                    for sgmc in sg_message_conn:
                        if cmds.objectType(sgmc) is 'RenderMan':
                            isAdaptExists = True
                            break
                if isAdaptExists:
                    om.MGlobal.displayInfo('Info: "rmanAdaptation" node for shader "%s" already exists.'%sg)
                    continue
                else:
                    rman_adapt_shdrs_list.append(sg)
                    blin_shdr = sg + '_blinn_shdr'
                    if '_REYES_' in blin_shdr:
                        blin_shdr = blin_shdr.replace('_REYES_', '_')
                    blin_shdr = cmds.shadingNode('blinn', asShader=True, name=blin_shdr)
                    blin_shdr_grp = sg + '_blinn_shdrSG'
                    if '_REYES_' in blin_shdr_grp:
                        blin_shdr_grp = blin_shdr_grp.replace('_REYES_', '_')
                    blin_shdr_grp = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=blin_shdr_grp)
                    cmds.connectAttr(blin_shdr + '.outColor', blin_shdr_grp + '.surfaceShader')
                    mel.eval('rmanExecAEMenuCmd("%s", "Add Adaptation")'%blin_shdr_grp)
                    rman_adapt = cmds.listConnections(blin_shdr_grp + '.rmanAdaptations[0]', source=True, destination=False)
                    if rman_adapt:
                        rman_adapt = rman_adapt[0]
                        cmds.setAttr(rman_adapt + '.rman__torattr___adaptorMatchString', 'Reyes', type='string')
                        cmds.connectAttr(sg + '.message', '%s.rman__torattr___customShadingGroup'%rman_adapt, force=True)
                        mel.eval('rmanSetAttr("%s", "rman__torattr___adaptorController", "$user:renderer");'%blin_shdr_grp)
                        curr_shdr = cmds.listConnections(sg + '.surfaceShader', source=True, destination=False)
                        if curr_shdr:
                            curr_shdr = curr_shdr[0]
                            color_file = ''
                            color_conn_list = []
                            try:
                                color_conn_list = cmds.listConnections(curr_shdr + '.surfaceColor', source=True, destination=False)
                            except Exception, err:
                                om.MGlobal.displayInfo('Info: Shader %s hasn\'t attribute "surfaceColor".'%curr_shdr)
                            if color_conn_list:
                                color_file_list = cmds.ls(color_conn_list, type='file')
                                if color_file_list:
                                    color_file = color_file_list[0]
                                else:
                                    color_conn_hist = cmds.listHistory(color_conn_list[0], pruneDagObjects=True)
                                    if color_conn_hist:
                                        color_conn_hist_file_list = cmds.ls(color_conn_hist, type='file')
                                        if color_conn_hist_file_list:
                                            color_file = color_conn_hist_file_list[0]
                                if color_file:
                                    color_path = cmds.getAttr(color_file + '.fileTextureName')
                                    new_texture_path = ''
                                    if color_path:
                                        color_texture_name = color_path.split('/')[-1]
                                        color_ext = os.path.splitext(color_texture_name)[1]
                                        new_texture_path = os.path.splitext(color_path)[0]+'.dds'
                                        if not 'cached' in color_path:
                                            color_folder = color_path.split('/')[-2]
                                            new_texture_path = new_texture_path.replace(color_folder + '/', color_folder + '/cached')
                                    tex_name = new_texture_path.split('/')[-1]
                                    if '_MAPID_' in new_texture_path:
                                        new_color_texture_list = pvGetTexFilesList(color_file, new_texture_path)
                                        if new_color_texture_list:
                                            pma_node = color_texture_name + '_pma'
                                            pma_node = cmds.createNode('plusMinusAverage', name=pma_node)
                                            for i, new_texture_path in enumerate(new_color_texture_list):
                                                tex_file_node, tex2d_node = pvCreateTexture(tex_name, new_texture_path)
                                                cmds.setAttr(tex2d_node + '.wrapU', 0)
                                                cmds.setAttr(tex2d_node + '.wrapV', 0)
                                                cmds.setAttr(tex2d_node + '.translateFrameU', i)
                                                cmds.setAttr(tex_file_node + '.defaultColor', 0, 0, 0, type='double3')
                                                cmds.connectAttr(tex_file_node + '.outColor', pma_node + '.input3D[%s]'%i, force=True)
                                            cmds.connectAttr(pma_node + '.output3D', blin_shdr + '.color', force=True)
                                    else:
                                        tex_file_node = pvCreateTexture(tex_name, new_texture_path)[0]
                                        cmds.connectAttr(tex_file_node + '.outColor', blin_shdr + '.color', force=True)

                    cmds.select(clear=True)
                    cmds.hyperShade(objects=sg)
                    selected = cmds.ls(sl=True)
                    cmds.sets(edit=True, forceElement=blin_shdr_grp)

    cmds.select(clear=True)
    om.MGlobal.displayInfo('Info: "Blinn" shaders created successfuly for renderman shaders: %s.'%rman_adapt_shdrs_list)
    return rman_adapt_shdrs_list

# pvCreateBlinToRman()