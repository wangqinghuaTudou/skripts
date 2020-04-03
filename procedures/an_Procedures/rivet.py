from  anProcedures import  an_unicName
import maya.cmds as cmds

def rivet(seurface='', edges=[], out = 'locator'):   
    if not seurface:
        sel = cmds.filterExpand (sm= 32)
        if not sel:
            cmds.error( "You mast select 2 edges" )
        seurface =  sel[0].split('.')[0]
        edges = [ x.split('[')[1].split(']')[0] for x in sel]

    pfx = an_unicName(seurface, '_riv', num=True )[0]
    nameCFME1 = cmds.createNode ( 'curveFromMeshEdge', n=pfx+"rivetCurveFromMeshEdge1")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(edges[0]))
    nameCFME2 = cmds.createNode ( 'curveFromMeshEdge', n=pfx+"rivetCurveFromMeshEdge2")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(edges[1]))
    nameLoft = cmds.createNode ( 'loft' , n=pfx+"rivetLoft1")
    cmds.setAttr (nameLoft+ ".ic", s=2)
    cmds.setAttr (nameLoft+  ".u", True)
    cmds.setAttr (nameLoft+  ".rsn", True)
    namePOSI = cmds.createNode ( 'pointOnSurfaceInfo' , n= pfx+"rivetPointOnSurfaceInfo1")
    cmds.setAttr ( ".turnOnPercentage", 1)
    cmds.setAttr ( ".parameterU", 0.5)
    cmds.setAttr ( ".parameterV", 0.5)
    cmds.connectAttr ( nameLoft + ".os",  namePOSI + ".is", f=True)
    cmds.connectAttr ( nameCFME1 + ".oc",  nameLoft + ".ic[0]")
    cmds.connectAttr ( nameCFME2 + ".oc",  nameLoft + ".ic[1]")
    cmds.connectAttr ( seurface + ".w",  nameCFME1 + ".im")
    cmds.connectAttr ( seurface + ".w",  nameCFME2 + ".im")
    if out =='locator': 
        nameLocator = cmds.createNode ( 'transform' , n = an_unicName ('rivet','' )[0]  )
        cmds.createNode ( 'locator' , n= nameLocator + "Shape", p=nameLocator)
    else:
        nameLocator = cmds.createNode ( 'joint' , n=pfx)
    
    nameAC = cmds.createNode ( 'aimConstraint', p= nameLocator , n=  nameLocator + "_rivetAimConstraint1")
    cmds.setAttr ( ".tg[0].tw", 1)
    cmds.setAttr ( ".a" , 0, 1, 0)
    cmds.setAttr ( ".u", 0, 0, 1)
    for attr in [".v", ".tx", ".ty", ".tz", ".rx", ".ry", ".rz", ".sx", ".sy", ".sz"]: cmds.setAttr ( attr, k=False)
    cmds.connectAttr ( namePOSI + ".position",   nameLocator + ".translate")
    cmds.connectAttr ( namePOSI + ".n",   nameAC + ".tg[0].tt")
    cmds.connectAttr ( namePOSI + ".tv",   nameAC + ".wu")
    for d in ('x', 'y', 'z'): cmds.connectAttr ( nameAC + ".cr"+d,   nameLocator + ".r"+d)
    return nameLocator
    
def getRivets():
    geo =  cmds.listRelatives( cmds.ls(sl=True)[0], s=True)[0]
    nods = [ x for x in cmds.listConnections(geo) if cmds.nodeType(x)=='curveFromMeshEdge']
    for tp in ( 'loft', 'pointOnSurfaceInfo', 'transform'):
        tmp =[]
        for y in nods: tmp.append( [ x for x in cmds.listConnections(y) if cmds.nodeType(x)== tp] [0]    )
        nods= list(set(tmp)) 
    return nods