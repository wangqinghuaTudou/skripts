import re
import time
import maya.cmds as cmds
import maya.OpenMaya as om

def PolyBridgeToExtrude( node=None ):

    volume_preserve = 'volumePreserve'

    if node:
        if not isinstance( node, ( list, tuple, dict, set )):
            node_list = [node]
        node_list = node
    else:
        node_list = cmds.ls( sl=True )
    
    result = {}
    for node in node_list:
        om.MGlobal.displayInfo ("Info: Create extrude geometry from \"" + str( node ) + "\"")
        shape = cmds.listRelatives( node, shapes=True )
        node_orig_shape = GetOriginalShape( node )
        if shape:
            shape = shape[0]
            history = cmds.listHistory( shape )
            if history:
                curve = cmds.ls( history, type="nurbsCurve" )
                if curve:
                    curve = curve[0]
                    bridge = cmds.ls( history, type="polyBridgeEdge" )
                    if bridge:
                        bridge = bridge[0]
                        skin_cluster = GetRelatedSkinCluster( node )
                        if skin_cluster:
                            curve_info = cmds.listConnections( curve + ".worldSpace[0]", type="curveInfo", source=False )
                            if curve_info:
                                range_node = cmds.listConnections( curve_info[0] + ".arcLength", source=False )
                                if range_node:
                                    range_node = range_node[0]
                                    taper_offset_node = cmds.listConnections( bridge + ".taper", destination=False )
                                    if taper_offset_node:
                                        taper_offset_node = taper_offset_node[0]
                                        inf = cmds.skinCluster( skin_cluster, inf=True, q=True )
                                        duplicate_node = cmds.duplicate( node )
                                        replace_name = re.sub( "Bridge", "Extrude", duplicate_node[0], 1, re.IGNORECASE )
                                        duplicate_node = cmds.rename( duplicate_node, replace_name )
                                        if duplicate_node[-1].isalnum():
                                            duplicate_node = cmds.rename( duplicate_node, duplicate_node[:-1] )
                                        bta_node = cmds.listConnections(node + '.squashSwitch', source=False, destination=True)
                                        if bta_node:
                                            bta_node = bta_node[0]
                                        if cmds.objExists(node + '.squashOffset') and cmds.objExists(duplicate_node + '.squashOffset'):
                                            squashOffset_connSource = cmds.listConnections(node + '.squashOffset', source=True, destination=False, plugs=True)
                                            if squashOffset_connSource:
                                                cmds.connectAttr(squashOffset_connSource[0], duplicate_node + '.squashOffset', force=True)
                                            squashOffset_connDestination = cmds.listConnections(node + '.squashOffset', source=False, destination=True, plugs=True)
                                            if squashOffset_connDestination:
                                                cmds.disconnectAttr(node + '.squashOffset', squashOffset_connDestination[0])
                                                cmds.connectAttr(duplicate_node + '.squashOffset', squashOffset_connDestination[0], force=True)
                                        if cmds.objExists(node + '.squashSwitch') and cmds.objExists(duplicate_node + '.squashSwitch'):
                                            squashSwitch_connSource = cmds.listConnections(node + '.squashSwitch', source=True, destination=False, plugs=True)
                                            if squashSwitch_connSource:
                                                cmds.connectAttr(squashSwitch_connSource[0], duplicate_node + '.squashSwitch', force=True)
                                            squashSwitch_connDestination = cmds.listConnections(node + '.squashSwitch', source=False, destination=True, plugs=True)
                                            if squashSwitch_connDestination:
                                                cmds.disconnectAttr(node + '.squashSwitch', squashSwitch_connDestination[0])
                                                cmds.connectAttr(duplicate_node + '.squashSwitch', squashSwitch_connDestination[0], force=True)
                                        duplicate_node_shape = cmds.listRelatives( duplicate_node, shapes=True)
                                        failed = False
                                        if duplicate_node_shape:
                                            duplicate_node_shape = duplicate_node_shape[0]
                                            duplicate_node_orig_shape = GetOriginalShape( duplicate_node )
                                            if cmds.objExists( duplicate_node_orig_shape ):
                                                cmds.delete( duplicate_node_orig_shape )
                                                cmds.connectAttr( node_orig_shape + ".worldMesh[0]", duplicate_node_shape + ".inMesh" )
                                                face_list = cmds.getAttr( duplicate_node_shape + ".face", mi=True )
                                                cmds.disconnectAttr( node_orig_shape + ".worldMesh[0]", duplicate_node_shape + ".inMesh" )
                                                if face_list:
                                                    cmds.delete( duplicate_node + ".f[" + str( face_list[len( face_list )/2]) + ":" + str( face_list[-1]) + "]")
                                                    face_list = face_list[( len(face_list)/2 )-1]
                                                    replace_skin_cluster = cmds.skinCluster( 
                                                        duplicate_node_shape,
                                                        inf,
                                                        toSelectedBones = True,
                                                        useGeometry = True,
                                                        dropoffRate = 4,
                                                        polySmoothness = False,
                                                        removeUnusedInfluence = False,
                                                        maximumInfluences = 5,
                                                        obeyMaxInfluences = False,
                                                        normalizeWeights = True
                                                    )[0]
                                                    extrude_node = cmds.polyExtrudeFacet( duplicate_node + ".f[0:" + str( face_list ) + "]", inc=curve, d=10 )[0]
                                                    twist_node = cmds.listConnections( bridge + ".twist" )
                                                    if twist_node:
                                                        cmds.connectAttr( twist_node[0] + ".rotateX", extrude_node + ".twist" )
                                                    volume_preserve_attribute = duplicate_node + '.' + volume_preserve
                                                    if not cmds.objExists( volume_preserve_attribute ):
                                                        cmds.addAttr( duplicate_node, longName=volume_preserve, attributeType='double', keyable=True )
                                                    cmds.setKeyframe( duplicate_node, attribute=volume_preserve, time=0, value=1 )
                                                    cmds.setKeyframe( duplicate_node, attribute=volume_preserve, time=8, value=1 )
                                                    cmds.keyTangent( duplicate_node, attribute=volume_preserve, weightedTangents=True )
                                                    cmds.keyTangent( duplicate_node, attribute=volume_preserve, weightLock=False )
                                                    cmds.keyTangent( volume_preserve_attribute, edit=True, absolute=True, time=(0, 0), outAngle=-25 )
                                                    cmds.keyTangent( volume_preserve_attribute, edit=True, absolute=True, time=(8, 8), outAngle=25 )
                                                    curve_length_mdv = cmds.createNode( 'multiplyDivide', name=taper_offset_node[:-3] + '_mdv' )
                                                    cmds.connectAttr( curve_info[0] + '.arcLength', curve_length_mdv + '.input1X' )
                                                    curve_length = cmds.getAttr( curve_length_mdv + '.input1X' )
                                                    cmds.setAttr( curve_length_mdv + '.input2X', curve_length )
                                                    cmds.setAttr( curve_length_mdv + '.operation', 2 )
                                                    curve_length_pma = cmds.createNode( 'plusMinusAverage', name=taper_offset_node[:-3] + '_pma' )
                                                    cmds.connectAttr( curve_length_mdv + '.outputX', curve_length_pma + '.input1D[0]' )
                                                    cmds.setAttr( curve_length_pma + '.input1D[1]', 1 )
                                                    cmds.setAttr( curve_length_pma + '.operation', 2 )
                                                    curve_length_k_mdl = cmds.createNode( 'multDoubleLinear', name=taper_offset_node[:-3] + 'K_mdl' )
                                                    cmds.connectAttr( curve_length_pma + '.output1D', curve_length_k_mdl + '.input1' )
                                                    cmds.setAttr( curve_length_k_mdl + '.input2', 3.1 )
                                                    cmds.setAttr( extrude_node + '.taperCurve[0].taperCurve_FloatValue', 1 )
                                                    cmds.setAttr( extrude_node + '.taperCurve[0].taperCurve_Position', 0 )
                                                    cmds.setAttr( extrude_node + '.taperCurve[0].taperCurve_Interp', 3 )
                                                    taper_curve_increment = 0.125
                                                    for i in xrange(7):
                                                        frame_cache_node = cmds.createNode( 'frameCache', name=taper_offset_node[:-3] + '%s_fc'%i )
                                                        cmds.connectAttr( volume_preserve_attribute, frame_cache_node + '.stream' )
                                                        cmds.setAttr( frame_cache_node + '.varyTime', i + 1 )
                                                        bta_curve_length_node = cmds.createNode( 'blendTwoAttr', name=taper_offset_node[:-3] + 'CurveLength%s_bta'%i )
                                                        #cmds.connectAttr( curve_length_pma + '.output1D', bta_curve_length_node + '.attributesBlender' )
                                                        cmds.connectAttr( curve_length_k_mdl + '.output', bta_curve_length_node + '.attributesBlender' )
                                                        cmds.connectAttr( frame_cache_node + '.varying', bta_curve_length_node + '.input[1]' )
                                                        cmds.setAttr( bta_curve_length_node + '.input[0]', 1 )
                                                        bta_user_switch_node = cmds.createNode( 'blendTwoAttr', name=taper_offset_node[:-3] + 'UserSwitch%s_bta'%i )
                                                        cmds.connectAttr( duplicate_node + '.squashSwitch', bta_user_switch_node + '.attributesBlender' )
                                                        cmds.connectAttr( bta_curve_length_node + '.output', bta_user_switch_node + '.input[1]' )
                                                        cmds.setAttr( bta_user_switch_node + '.input[0]', 1 )
                                                        adl_manual_offset_node = cmds.createNode( 'addDoubleLinear', name=taper_offset_node[:-3] + 'ManualOffset%s_adl'%i )
                                                        cmds.connectAttr( bta_user_switch_node + '.output', adl_manual_offset_node + '.input1' )
                                                        cmds.connectAttr( duplicate_node + '.squashOffset', adl_manual_offset_node + '.input2' )
                                                        cmds.connectAttr( adl_manual_offset_node + '.output', extrude_node + '.taperCurve[%s].taperCurve_FloatValue'%(i + 1) )
                                                        cmds.setAttr( extrude_node + '.taperCurve[%s].taperCurve_Position'%(i + 1), taper_curve_increment )
                                                        cmds.setAttr( extrude_node + '.taperCurve[%s].taperCurve_Interp'%(i + 1), 3 )
                                                        taper_curve_increment += 0.125
                                                    cmds.setAttr( extrude_node + '.taperCurve[8].taperCurve_FloatValue', 1 )
                                                    cmds.setAttr( extrude_node + '.taperCurve[8].taperCurve_Position', 1 )
                                                    cmds.setAttr( extrude_node + '.taperCurve[8].taperCurve_Interp', 3 )
                                                    result[duplicate_node] = TransferSkinClusterInfluence( node, duplicate_node )
                                                    om.MGlobal.displayInfo ('Info: "%s" successfully converted.'%duplicate_node)
                                                    cmds.delete(node)
                                                    om.MGlobal.displayInfo ('Info: "%s" deleted.'%node)
                                                else:
                                                    failed = True
                                            else:
                                                failed = True
                                        else:
                                            failed = True
                                        if failed:
                                            cmds.delete( duplicate_node )
                    else:
                        om.MGlobal.displayWarning ("Warning: \"" + str( shape ) + "\" has no contain any bridge node in history.")
                else:
                    om.MGlobal.displayWarning ("Warning: \"" + str( shape ) + "\" has no contain any nurbsCurve in history.")
            else:
                om.MGlobal.displayWarning ("Warning: \"" + str( shape ) + "\" has no history.")
        else:
            om.MGlobal.displayWarning ("Warning: \"" + str( node ) + "\" has no any child.")
    return result
    
def TransferSkinClusterInfluence( source, target ):
    
    om.MGlobal.displayInfo ("Info: Transfer influence.")
    result = []
    if cmds.ls( source, type="transform" ) and cmds.ls( target, type="transform" ):
        connections = cmds.listConnections( source + ".worldMatrix[0]", source=False )
        skin_cluster_list = []
        if connections:
            skin_cluster_list = cmds.ls( connections, type="skinCluster" )
        if skin_cluster_list:
            skin_cluster_list = set( skin_cluster_list )
            size = len( skin_cluster_list )
            skin_cluster_counter = 0
            for skin_cluster in skin_cluster_list:
                om.MGlobal.displayInfo ('Info: ( %s/%s ) Transfer "%s"'%(skin_cluster_counter+1, size, skin_cluster))
                sourceIndex = GetInfluenceIndex ( source, skin_cluster )
                if source in cmds.skinCluster( skin_cluster, query=True, influence=True ):
                    geometry = cmds.skinCluster( skin_cluster, query=True, geometry=True )
                    if geometry:
                        geometry = geometry[0]
                        vertices_number = cmds.polyEvaluate( geometry, vertex=True )
                        om.MGlobal.displayInfo ("Info: Update influence.")
                        cmds.skinCluster( skin_cluster, edit=True, addInfluence=target, useGeometry=True, weight=0 )
                        weights_list = cmds.getAttr (skin_cluster + ".weightList[0:%s].w[%s]"%(vertices_number, sourceIndex))
                        targetIndex = GetInfluenceIndex ( target, skin_cluster )
                        for i, wl in enumerate(weights_list):
                            if wl > 0:
                                cmds.setAttr (skin_cluster + '.weightList[%s].w[%s]'%(i, targetIndex), wl )
                        om.MGlobal.displayInfo ("Info: Remove original influence.")
                        cmds.skinCluster( skin_cluster, edit=True, removeInfluence=[source] )
                        result.append( skin_cluster )
                        cmds.select(clear=True)
                    else:
                        om.MGlobal.displayWarning ("Warning: \"" + skin_cluster + "\" has not any geometry.")
                else:
                    om.MGlobal.displayWarning ("Warning: \"" + source_shape + "\" has not influence node.")
                skin_cluster_counter += 1
        else:
            om.MGlobal.displayWarning ("Warning: \"" + source_shape + "\" has not contain any skinCluster node.")
    else:
        om.MGlobal.displayWarning ("Warning: \"" + source_shape + "\" is not transform node.")
    om.MGlobal.displayInfo ("Info: Influence transfered.")
    return result
    
def GetOriginalShape ( node ):
    shapes = cmds.listRelatives( node, shapes=True)
    if not shapes:
        om.MGlobal.displayInfo ('Node "%s" has no shape(s).')
        return False
    orig_shapes_list = []
    for shp in shapes:
        if cmds.getAttr(shp + '.intermediateObject'):
            orig_shapes_list.append(shp)
    if not orig_shapes_list:
        om.MGlobal.displayInfo ('Node "%s" has no "Orig" shape(s).')
        return False
    return orig_shapes_list[-1]

def GetInfluenceIndex ( node, skin_cluster ):
    skinConnections = cmds.listConnections( node + ".worldMatrix[0]", source=False, destination=True, plugs=True )
    if skinConnections:
        for sc in skinConnections:
            if skin_cluster in sc:
                sc_parts = sc.split('.')[1]
                influenceIndex = sc_parts[7:-1]
    return influenceIndex

def GetRelatedSkinCluster( node ):

    hidden_shape = None
    hidden_shape_with_parent = None
    skin_shape = None
    skin_shape_with_parent = None
    if cmds.ls( node, type="controlPoint" ):
        skin_shape = node
    else:
        relative_list = cmds.listRelatives( node )
        if relative_list:
            for relative in relative_list:
                if not cmds.ls( relative, type="controlPoint" ):
                    continue
                if cmds.getAttr( node + "|" + relative + ".io" ):
                    continue
                visibility = cmds.getAttr( node + "|" + relative + ".v" )
                if not visibility:
                    hidden_shape = relative
                    hidden_shape_with_parent = node + "|" + relative
                    continue
                skin_shape = relative
                skin_shape_with_parent = node + "|" + relative
                break
    if not skin_shape:
        if not hidden_shape:
            return None
        else:
            skin_shape = hidden_shape
            skin_shape_with_parent = hidden_shape_with_parent
    for skin_cluster in cmds.ls( type="skinCluster" ):
        geometry_list = cmds.skinCluster( skin_cluster, query=True, geometry=True )
        if geometry_list:
            for geometry in geometry_list:
                if geometry == skin_shape or geometry == skin_shape_with_parent:
                    return skin_cluster
    return True

timeStart = time.time()
PolyBridgeToExtrude()
timeStop = time.time()
om.MGlobal.displayInfo ('Info: Execution time - %s seconds.'%(timeStop - timeStart))