import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

def pvFixTexturesPaths():

    files_list = cmds.ls(type='file')
    if files_list:
        for f in files_list:
            tex_path = cmds.getAttr(f + '.fileTextureName')
            if len(tex_path) > 0:
                if tex_path[0] == '/':
                    if tex_path[1] != '/':
                        new_tex_path = '/' + tex_path
                        cmds.setAttr(f + '.fileTextureName', new_tex_path, type='string')
                        om.MGlobal.displayInfo('Info: Texture\'s path successfuly fixed for "%s".'%f)

def pvSetRenderAttributes(*args):

    if not args:
        args = cmds.ls(selection=True)
    if not args:
        om.MGlobal.displayWarning('Must be specified any object(s).')
        return

    renderAttributesList = ['.castsShadows', \
                            '.receiveShadows', \
                            '.motionBlur', \
                            '.primaryVisibility', \
                            '.smoothShading', \
                            '.visibleInReflections', \
                            '.visibleInRefractions', \
                            '.motionBlur', \
                            '.doubleSided']

    mesh_list = args[0]
    for msh in mesh_list:
        for rna in renderAttributesList:
            try:
                cmds.setAttr(msh + rna, 1)
            except Exception, err:
                om.MGlobal.displayWarning(err)

def pvCreateRmanTextue(sg='simpleRmanSG', new_tex_path=''):

    rman_file = sg + 'rman_file'
    rman_2dtex = sg + 'rman_2dtex'
    rman_file = cmds.shadingNode('file', asTexture=True, isColorManaged=True, name=rman_file)
    rman_2dtex = cmds.shadingNode('place2dTexture', asUtility=True, name=rman_2dtex)
    cmds.connectAttr(rman_2dtex + '.coverage', rman_file + '.coverage', force=True)
    cmds.connectAttr(rman_2dtex + '.translateFrame', rman_file + '.translateFrame', force=True)
    cmds.connectAttr(rman_2dtex + '.rotateFrame', rman_file + '.rotateFrame', force=True)
    cmds.connectAttr(rman_2dtex + '.mirrorU', rman_file + '.mirrorU', force=True)
    cmds.connectAttr(rman_2dtex + '.mirrorV', rman_file + '.mirrorV', force=True)
    cmds.connectAttr(rman_2dtex + '.stagger', rman_file + '.stagger', force=True)
    cmds.connectAttr(rman_2dtex + '.wrapU', rman_file + '.wrapU', force=True)
    cmds.connectAttr(rman_2dtex + '.wrapV', rman_file + '.wrapV', force=True)
    cmds.connectAttr(rman_2dtex + '.repeatUV', rman_file + '.repeatUV', force=True)
    cmds.connectAttr(rman_2dtex + '.offset', rman_file + '.offset', force=True)
    cmds.connectAttr(rman_2dtex + '.rotateUV', rman_file + '.rotateUV', force=True)
    cmds.connectAttr(rman_2dtex + '.noiseUV', rman_file + '.noiseUV', force=True)
    cmds.connectAttr(rman_2dtex + '.vertexUvOne', rman_file + '.vertexUvOne', force=True)
    cmds.connectAttr(rman_2dtex + '.vertexUvTwo', rman_file + '.vertexUvTwo', force=True)
    cmds.connectAttr(rman_2dtex + '.vertexUvThree', rman_file + '.vertexUvThree', force=True)
    cmds.connectAttr(rman_2dtex + '.vertexCameraOne', rman_file + '.vertexCameraOne', force=True)
    cmds.connectAttr(rman_2dtex + '.outUV', rman_file + '.uv', force=True)
    cmds.connectAttr(rman_2dtex + '.outUvFilterSize', rman_file + '.uvFilterSize', force=True)
    cmds.setAttr(rman_file + '.fileTextureName', new_tex_path, type='string')
    return rman_file, rman_2dtex

def pvCreateRendermanAdaptation():

    pvFixTexturesPaths()

    if cmds.objExists('geometry_grp'):
        geo_grp = 'geometry_grp'
        mesh_list = cmds.listRelatives(geo_grp, allDescendents=True, type='mesh', noIntermediate=True, fullPath=True)
        if mesh_list:
            pvSetRenderAttributes(mesh_list)
    if cmds.objExists('geo_normal'):
        geo_grp = 'geo_normal'
        mesh_list = cmds.listRelatives(geo_grp, allDescendents=True, type='mesh', noIntermediate=True, fullPath=True)
        if mesh_list:
            pvSetRenderAttributes(mesh_list)
    if cmds.objExists('geo_middle'):
        geo_grp = 'geo_middle'
        mesh_list = cmds.listRelatives(geo_grp, allDescendents=True, type='mesh', noIntermediate=True, fullPath=True)
        if mesh_list:
            pvSetRenderAttributes(mesh_list)

    sg_list = cmds.ls(type='shadingEngine')
    if not sg_list:
        om.MGlobal.displayWarning('Can not find any "Shading Engine" node.'),
    else:
        rman_adapt_shdrs_list = []
        for sg in sg_list:
            print('Info: sg - %s'%sg)
            if cmds.objExists(sg + '.rmanAdaptations[0]'):
                om.MGlobal.displayInfo('"rmanAdaptations" attribute for shader "%s" already exists.'%sg)
                continue
            else:
                rman_adapt_shdrs_list.append(sg)
                mel.eval('rmanExecAEMenuCmd("%s", "Add Adaptation")'%sg)
                rman_adapt = cmds.listConnections(sg + '.rmanAdaptations[0]', source=True, destination=False)
                if rman_adapt:
                    rman_adapt = rman_adapt[0]
                    print('Info: rman_adapt - %s'%rman_adapt)
                    rmsgp_shdr = sg + '_rmsgp_shdr'
                    rmsgp_shdr = cmds.shadingNode('RMSGPSurface', asShader=True, name=rmsgp_shdr)
                    print('Info: rmsgp_shdr - %s'%rmsgp_shdr)
                    rmsgp_shdr_grp = sg + '_rmsgp_shdrSG'
                    cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=rmsgp_shdr_grp)
                    print('Info: rmsgp_shdr_grp - %s'%rmsgp_shdr_grp)
                    cmds.connectAttr(rmsgp_shdr + '.outColor', rmsgp_shdr_grp + '.surfaceShader')
                    cmds.setAttr(rman_adapt + '.rman__torattr___adaptorMatchString', 'Reyes', type='string')
                    cmds.connectAttr(rmsgp_shdr_grp + '.message', '%s.rman__torattr___customShadingGroup'%rman_adapt, force=True)
                    mel.eval('rmanSetAttr("%s", "rman__torattr___adaptorController", "$user:renderer");'%sg)
                    curr_shdr = cmds.listConnections(sg + '.surfaceShader', source=True, destination=False)
                    if curr_shdr:
                        print('Info: curr_shdr - %s'%curr_shdr)
                        shdr_hist = cmds.listHistory(curr_shdr[0], pruneDagObjects=True)
                        if shdr_hist:
                            print('Info: shdr_hist - %s'%shdr_hist)
                            files_list = cmds.ls(shdr_hist, type='file')
                            if files_list:
                                if len(files_list) > 1:
                                    pma_node = curr_shdr[0] + '_pma'
                                    pma_node = cmds.createNode('plusMinusAverage', name=pma_node)
                                    print('Info: pma_node - %s'%pma_node)
                                    for i, tex_file in enumerate(files_list):
                                        print('Info: tex_file - %s'%tex_file)
                                        tex_path = cmds.getAttr(tex_file + '.fileTextureName')
                                        new_tex_path = ''
                                        if tex_path:
                                            tex_ext = tex_path.split('.')[1]
                                            new_tex_path = tex_path.replace(tex_ext, 'tex')
                                            if not 'cached' in tex_path:
                                                tex_folder = tex_path.split('/')[-2]
                                                new_tex_path = new_tex_path.replace(tex_folder + '/', tex_folder + '/cached')
                                        rman_file, rman_2dtex = pvCreateRmanTextue(sg, new_tex_path)
                                        tex_file_hist = cmds.listHistory(tex_file, pruneDagObjects=True)
                                        if tex_file_hist:
                                            print('Info: tex_file_hist - %s'%tex_file_hist)
                                            curr_2dtex = cmds.ls(type='place2dTexture')
                                            if curr_2dtex:
                                                print('Info: curr_2dtex - %s'%curr_2dtex)
                                                wrap_u = cmds.getAttr(curr_2dtex[0] + '.wrapU')
                                                wrap_v = cmds.getAttr(curr_2dtex[0] + '.wrapV')
                                                tr_frame_u = cmds.getAttr(curr_2dtex[0] + '.translateFrameU')
                                                tr_frame_v = cmds.getAttr(curr_2dtex[0] + '.translateFrameV')
                                                cmds.setAttr(rman_2dtex + '.wrapU', wrap_u)
                                                cmds.setAttr(rman_2dtex + '.wrapV', wrap_v)
                                                cmds.setAttr(rman_2dtex + '.translateFrameU', tr_frame_u)
                                                cmds.setAttr(rman_2dtex + '.translateFrameV', tr_frame_v)
                                        print('Info: rman_file - %s'%rman_file)
                                        cmds.connectAttr(rman_file + '.outColor', pma_node + '.input3D[%s]'%i, force=True)
                                    cmds.connectAttr(pma_node + '.output3D', rmsgp_shdr + '.surfaceColor', force=True)
                                else:
                                    tex_file = files_list[0]
                                    print('Info: tex_file - %s'%tex_file)
                                    tex_path = cmds.getAttr(tex_file[0] + '.fileTextureName')
                                    new_tex_path = ''
                                    if tex_path:
                                        tex_ext = tex_path.split('.')[1]
                                        new_tex_path = tex_path.replace(tex_ext, 'tex')
                                        if not 'cached' in tex_path:
                                            tex_folder = tex_path.split('/')[-2]
                                            new_tex_path = new_tex_path.replace(tex_folder + '/', tex_folder + '/cached')
                                    rman_file = pvCreateRmanTextue(sg, new_tex_path)[0]
                                    print('Info: rman_file - %s'%rman_file)
                                    cmds.connectAttr(rman_file + '.outColor', rmsgp_shdr + '.surfaceColor', force=True)

    om.MGlobal.displayInfo('Renderman adaption nodes created successfuly for shaders: %s.'%rman_adapt_shdrs_list)
    return True

# pvCreateRendermanAdaptation()