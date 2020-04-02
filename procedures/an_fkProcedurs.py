import maya.cmds as cmds
from anProcedures import *
from CharacterNames import CharacterNames as chn
from an_classControllers import AnControllers as ctrl



'''
        an_fkProcedurs()

an_fkControllerss()          -   put controlers to plase and connect jnt to parent
an_fkToJntDevider()          - 

ikPointRigSys( ) 

'''


def an_fkController( name, jnt, p=None, pType='constraint'): 
    obj = ctrl(name)
    obj.makeController ( shapeType= "fk", size=1, offset =[0, 0, 0], orient="X", pos=jnt, posType='parent')
    if p and pType=='constraint':   
        cmds.parentConstraint(p, obj.oriGrp, mo = True)

def an_fkToJntDevider(ct, jnts):
    mpdv = cmds.createNode ('multiplyDivide',  n = chn(ct).sfxMinus()+'_mpdv') 
    setAttr (mpdv+".operation", 2) 
    cmds.addAttr (ct, longName='mult', dv=1,  keyable=True) 
    for d in  ['x', 'y', 'z']:
        cmds.connectAttr (ct+'.mult',   mpdv+".input2"+d.upper()) 
        cmds.connectAttr (ct+'.r'+d  , mpdv+'.input1'+d.upper())
        for jnt in jnts:
            cmds.connectAttr(mpdv+'.output'+d.upper(), jnt+'.rotate'+d.upper())


"""___________________________________________________________________________________________________________________________ 

 
"""

def ikPointRigSys(pfx='r_stretchZone', jntNum=10, ctSize=1):
    
    jnts= cmds.ls(sl=1)
    rigGrp = cmds.group(em=True, n=pfx+'Rig_grp') 
    jntList=[]
    ctObjects = []
    for i in xrange(len(jnts)): 
        ctObj=ctrl(pfx+str(i)+chn('').suffixes[0]) #define ct name
        ctObjects.append(ctObj)
        ctObj.makeController( 'fk', ctSize)
        ctObj.rotateCt([0, -90, 90])
        ctObj.hideAttr([ 'sx', 'sy', 'sz', 'v'])
        jnt = cmds.joint(n=pfx+str(i)+chn('').suffixes[1]  ) 
        jntList.append(jnt)
        cmds.parent(jnt, ctObj.name) 
        cmds.parent(ctObj.oriGrp, rigGrp)     
        ctObj.placeCT ( jnts[i]  , 'parent')   # place CT

    nPlane = nurbsPlaneOnJnt(jntList)
    riv = rivetJntOnPlane(nPlane,  jntNum, pfx)
    sk_plane = cmds.duplicate( riv[1], n=pfx+'Skin_pln')[0]
    for pln in [ nPlane, riv[1], sk_plane]:
        cmds.setAttr (pln+".inheritsTransform",  0)
        cmds.setAttr (pln+".v",  0)
        cmds.parent(pln, rigGrp)
    cmds.setAttr (sk_plane+".v",  1)
    cmds.skinCluster(sk_plane, riv[0], toSelectedBones=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, rui=False, mi=5, omi =False, normalizeWeights=True)[0] 
    
    cmds.addAttr (rigGrp, longName='Scale', dv=1,  keyable=True) 
    for each in riv[0]:
        for d in 'X', 'Y', 'Z':
            cmds.connectAttr(rigGrp+'.Scale', each +'.'+'scale'+d)


def fkRigForSelJnt(pfx='test', jntNum=8):    
    jntList= cmds.ls(sl=1)
    cSize = an_distans(jntList[0], jntList[1])
    ttt = an_fkRig( jntList[1:], pfx=pfx, ctSize=cSize)
    fkRigGrp = pfx+'FkRig_grp'
    nPlane = nurbsPlaneOnJnt(jntList)
    riv = rivetJntOnPlane(nPlane,  jntNum=jntNum, pfx=pfx)
    sk_plane = cmds.duplicate( riv[1], n=pfx+'Skin_pln')[0]
    for pln in [ nPlane, riv[1], sk_plane]:
        cmds.setAttr (pln+".inheritsTransform",  0)
        cmds.setAttr (pln+".v",  0)
        cmds.parent(pln, fkRigGrp)
    cmds.setAttr (sk_plane+".v",  1)
    cmds.skinCluster(sk_plane, riv[0], toSelectedBones=True, useGeometry=True, dropoffRate=4, polySmoothness=False, nurbsSamples=25, rui=False, mi=5, omi =False, normalizeWeights=True)[0] 
    cmds.parentConstraint(jntList[0], fkRigGrp,  mo=True)
    
def nurbsPlaneOnJnt(jntList, pfx=''):
    if not pfx: pfx=chn(jntList[0]).sfxMinus()
    prWeight = an_distans (jntList[0], jntList[-1])/20 
    profilsList=[]
    for jnt in jntList:
        crv = cmds.curve(d=1, p=((0, 0, prWeight),   (0, 0, prWeight*-1)))
        cmds.parentConstraint( jnt, crv, mo=False)
        profilsList.append(crv)
    nPlane = cmds.loft( profilsList, n=pfx+'_nPlane', ch=True, rn=True, ar=True )[0]    
    cmds.delete (profilsList)
    cmds.skinCluster(nPlane, jntList, dr=4.5)
    return nPlane

def rivetJntOnPlane(nPlane,  jntNum=15, pfx=''):
    if not pfx: pfx=chn(jntList[0]).sfxMinus()
    polySkin = cmds.nurbsToPoly (nPlane, n=pfx+'_pPlane',  mnd=1, ch=1, f=2, pt=1, pc=200, chr=0.9, ft=0.01, mel=0.001, d=0.1, ut=1, un=jntNum, vn=2, vt=1, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
    rivetJnt=[]
    for i in range (0, jntNum-1):
        adges = cmds.polyInfo(polySkin+'.f['+str(i)+']', faceToEdge=True )[0].split(':')[1].split(' ')
        edgeList = [x for x in  adges  if x and x != '\n']
        rivet = an_rivetJnt(polySkin, edgeList[1], edgeList[3])
        rivetJnt.append(rivet)
    rivetGrp = cmds.group(rivetJnt, n=pfx+'Rivet_grp')
    return rivetJnt, polySkin


def an_rivetJnt(nameObject, e1, e2):  # e1, e2 - nambers of edges
    v_prefix = an_unicName(nameObject, '_riv', num=True )[0]
    nameCFME1 = cmds.createNode ( 'curveFromMeshEdge', n=v_prefix+"rivetCurveFromMeshEdge1")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e1))
    nameCFME2 = cmds.createNode ( 'curveFromMeshEdge', n=v_prefix+"rivetCurveFromMeshEdge2")
    cmds.setAttr ( ".ihi", 1)
    cmds.setAttr ( ".ei[0]",   int(e2))
    nameLoft = cmds.createNode ( 'loft' , n=v_prefix+"rivetLoft1")
    cmds.setAttr (nameLoft+ ".ic", s=2)
    cmds.setAttr (nameLoft+  ".u", True)
    cmds.setAttr (nameLoft+  ".rsn", True)
    namePOSI = cmds.createNode ( 'pointOnSurfaceInfo' , n= v_prefix+"rivetPointOnSurfaceInfo1")
    cmds.setAttr ( ".turnOnPercentage", 1)
    cmds.setAttr ( ".parameterU", 0.5)
    cmds.setAttr ( ".parameterV", 0.5)
    cmds.connectAttr ( nameLoft + ".os",  namePOSI + ".is", f=True)
    cmds.connectAttr ( nameCFME1 + ".oc",  nameLoft + ".ic[0]")
    cmds.connectAttr ( nameCFME2 + ".oc",  nameLoft + ".ic[1]")
    cmds.connectAttr ( nameObject + ".w",  nameCFME1 + ".im")
    cmds.connectAttr ( nameObject + ".w",  nameCFME2 + ".im")
    
    nameLocator = cmds.createNode ( 'joint' , n=v_prefix)
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


