import maya.cmds as mc
from pvCopySkinWeights import *
import pvProcedures as pvp
import re
import maya.api.OpenMaya as om 

def pvCopySkinToSelVertices():
    destVertices = mc.ls(selection=True, flatten=True) # getting selected vertices list
    sourceGeo = destVertices.pop(-1) # getting source geometry name
    rex = re.compile(r'^(([a-zA-Z0-9_]*).(vtx\[[0-9]*\]))$') # compile constructed vertex name
    lookLike = rex.match(destVertices[0])
    if lookLike:
        destGeo = lookLike.groups()[1] # getting destination geometry name
    else:
        destGeo = sourceGeo

# making source geometry's duplicate and copy skinWeights on them from source
    dupGeo = mc.duplicate(destGeo, rr=True)[0]
    mc.select([sourceGeo, dupGeo], replace=True)
    pvCopySkinWeightsMain()

    dupSkin = pvp.pvGetSkinCluster(dupGeo) # getting name of duplicated skinning
    destSkin = pvp.pvGetSkinCluster(destGeo) # getting name of destination skinning
    dupJnts = mc.skinCluster(dupSkin, query=True, influence=True) # getting list of duplicated skin influences
    destJnts = mc.skinCluster(destSkin, query=True, influence=True) # getting list of destination skin influences

# find difference in joints lists and add missing joints from duplicate skinning to destination skinning
    addJnts = list(set(dupJnts) - set(destJnts))
    if addJnts:
        mc.skinCluster(destSkin, \
                       edit=True, \
                       useGeometry=True, \
                       dropoffRate=4, \
                       polySmoothness=False, \
                       nurbsSamples=25, \
                       lockWeights=True, \
                       weight=0, \
                       addInfluence=addJnts)

# copy skin weights from slected vertexes on duplicated geometry to destination geometry
    for dVtx in destVertices:
        dpVtx = dVtx.replace(destGeo, dupGeo) # getting name of duplicated vertix corresponding with destination vertix
        destTV = []
        for dpJnt in dupJnts:
            mc.setAttr('%s.liw'%dpJnt, 0) # unlock joint in the skinning
            vtxWeight = mc.skinPercent(dupSkin, \
                                       dpVtx, \
                                       query=True, \
                                       transform=dpJnt) # getting value of the dup join on the dup vertix
            destTV.append((dpJnt, vtxWeight)) # making list of joints and corresponding values for each vertix
        mc.skinPercent(destSkin, dVtx, transformValue=destTV) # setting values from the list of corresponding joints on to the dest vertix 

    mc.delete(dupGeo) # delete duplicate geometry
    mc.select(clear=True) # clear selection
    om.MGlobal.displayInfo('Skin weights successfuly copied from "%s" to selected vertices on "%s".'%(sourceGeo, destGeo))

# pvCopySkinToSelVertices()