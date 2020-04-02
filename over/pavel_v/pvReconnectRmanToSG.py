import maya.cmds as cmds
import maya.OpenMaya as om

def pvReconnectRmanToSG():

    om.MGlobal.displayInfo('Info: ----------------------------------------------------------------')
    om.MGlobal.displayInfo('Info: Start to fix "Renderman" shaders connections to "ShadingGroups".')
    rman_is_loaded = cmds.pluginInfo('RenderMan_for_Maya', query=True, loaded=True)
    if not rman_is_loaded:
        om.MGlobal.displayInfo('Info: "Renderman" plugin not loaded.')
        try:
            om.MGlobal.displayInfo('Info: Trying to load "Renderman" plugin.')
            cmds.loadPlugin('RenderMan_for_Maya.mll')
        except:
            om.MGlobal.displayInfo('Info: Can\'t load "Renderman" plugin.')
            return False

    om.MGlobal.displayInfo('Info: "Renderman" plugin loaded successfuly.')
    rman_shdrs_list = cmds.ls(type='RMSGPSurface')
    if rman_shdrs_list:
        for rman_shdr in rman_shdrs_list:
            om.MGlobal.displayInfo('Info: "Renderman" shader - "%s".'%rman_shdr)
            rman_shdr_conn = cmds.listConnections(rman_shdr, source=False, destination=True)
            if rman_shdr_conn:
                rman_adapt = False
                for rsc in rman_shdr_conn:
                    if 'RenderMan' in cmds.objectType(rsc) and 'rmanAdaptation' in rsc and cmds.listConnections('%s.message'%rsc):
                        rman_adapt = True
                        break
                if not rman_adapt:
                    rman_shdr_conn_out = cmds.listConnections(rman_shdr, source=False, destination=True)
                    if not rman_shdr_conn_out:
                        om.MGlobal.displayInfo('Info: "Renderman" shader doesn\'t have output connections.')
                    else:
                        rs_material = cmds.ls(rman_shdr_conn_out, type='RedshiftMaterial')
                        if not rs_material:
                            om.MGlobal.displayInfo('Info: "Renderman" shader doesn\'t have "Redshift" meterial in output connections.')
                        else:
                            rs_shdr_future = cmds.listHistory(rs_material, future=True)
                            if not rs_shdr_future:
                                om.MGlobal.displayInfo('Info: "Redshift" meterial doesn\'t have future connections.')
                            else:
                                shading_engine = cmds.ls(rs_shdr_future, type='shadingEngine')
                                if not shading_engine:
                                    om.MGlobal.displayWarning('Info: Shading network hasn\'t "Shading Engine".')
                                else:
                                    adapt_creation = False
                                    try:
                                        mel.eval('rmanExecAEMenuCmd("%s", "Add Adaptation")'%shading_engine[0])
                                        om.MGlobal.displayInfo('Info: "Renderman" adaptation successfuly created.')
                                        adapt_creation = True
                                    except:
                                        om.MGlobal.displayWarning('Info: Can\'t create "renderman" adaptation.')
                                    if adapt_creation:
                                        rman_sg_node = cmds.listConnections('%s.outColor'%rman_shdr, source=False, destination=True)
                                        if rman_sg_node:
                                            rman_sg_node = rman_sg_node[0]
                                        else:
                                            rman_sg_node_name = '%sSG'%rman_shdr
                                            rman_sg_node = cmds.createNode('shadingEngine', name=rman_sg_node_name)
                                            cmds.connectAttr('%s.outColor'%rman_shdr, '%s.surfaceShader'%rman_sg_node, force=True)
                                        rman_adapt_node = cmds.listConnections('%s.rmanAdaptations'%shading_engine[0], source=True, destination=False, type='RenderMan')
                                        if rman_adapt_node:
                                            rman_adapt_node = rman_adapt_node[0]
                                            cmds.setAttr('%s.rman__torattr___adaptorMatchString'%rman_adapt_node, 'Reyes', type='string')
                                            cmds.connectAttr('%s.message'%rman_sg_node, '%s.rman__torattr___customShadingGroup'%rman_adapt_node, force=True)
                                            mel.eval('rmanSetAttr("%s", "rman__torattr___adaptorController", "$user:renderer");'%shading_engine[0])

    om.MGlobal.displayInfo('Info: Fixing "Renderman" shaders connections to "ShadingGroups" successfuly complete.')
    om.MGlobal.displayInfo('Info: -------------------------------------------------------------------------------')
    return True

# pvReconnectRmanToSG()