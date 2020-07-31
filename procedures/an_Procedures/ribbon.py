
#!/usr/bin/env python
# -*- coding: utf-8 -*-


import maya.cmds as cmds
from anProcedures import *
from CharacterNames import CharacterNames as chn
from an_classControllers import AnControllers as ctrl
from  an_Procedures.rivet import  rivet


'''
             ribbon

ikPointRigSys( )             -  ������� ������ ������� ���� ������. 
sortPolyFaceseLine()         -  ���������� ������������������ ������ �� 0 
faceToOppositEdges(face)     -  ����������� ��������� ���� � �������������� �����
'''

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
    
def nurbsPlaneOnJnt(jntList, pfx='', geo = 'nurbs'):
    if not pfx: pfx=chn(jntList[0]).sfxMinus()
    prWeight = an_distans (jntList[0], jntList[-1])/20 
    profilsList=[]
    for jnt in jntList:
        crv = cmds.curve(d=1, p=((0, 0, prWeight),   (0, 0, prWeight*-1)))
        cmds.parentConstraint( jnt, crv, mo=False)
        profilsList.append(crv)
    nPlane = cmds.loft( profilsList, n=pfx+'_nPlane', ch=True, rn=True, ar=True)[0]  
    if not geo == 'nurbs':
        nPlane = cmds.nurbsToPoly(nPlane, n=pfx+'_pPlane', pc=len(jntList), f=3, un=len(jntList), pt=1 )[0]
        cmds.delete (pfx+'_nPlane')
    cmds.delete (profilsList)
    cmds.skinCluster(nPlane, jntList, dr=4.5)
    return nPlane

def rivetJntOnPlane(nPlane,  jntNum=15, pfx=''):
    if not pfx: pfx=chn(jntList[0]).sfxMinus()
    polySkin = cmds.nurbsToPoly (nPlane, n=pfx+'_pPlane',  mnd=1, ch=1, f=2, pt=1, pc=200, chr=0.9, ft=0.01, mel=0.001, d=0.1, ut=1, un=jntNum, vn=2, vt=1, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)[0]
    rivetJnt=[]
    for i in sortPolyFaceseLine(geo):
        adges = faceToOppositEdges(polySkin+'.f['+str(i)+']')
        rvt = rivet(polySkin, [adges[0], adges[1]], out="joint")
        rivetJnt.append(rvt)
    rivetGrp = cmds.group(rivetJnt, n=pfx+'Rivet_grp')
    return rivetJnt, polySkin
    
def sortPolyFaceseLine(geo):
    fNum = cmds.polyEvaluate(geo, f=True )
    fDic ={}
    for i in range(fNum):
        adges = an_convertSliceToList(cmds.polyListComponentConversion(geo+'.f['+str(i)+']', toEdge=True ))
        fDic[i]= [int(x.split('[')[1][:-1]) for x in adges ]
    curF=0
    fList=[]
    for _ in range(fNum):
        fList.append(curF)
        c_val = set(fDic.pop(curF))
        for f in  fDic.keys():
            if c_val.intersection( set(fDic[f])): curF=f 
    return fList  
 
def faceToOppositEdges(face):
    adges = an_convertSliceToList(cmds.polyListComponentConversion(face, toEdge=True ))
    vert = an_convertSliceToList(cmds.polyListComponentConversion(adges[0], toVertex=True ))
    adges2 = an_convertSliceToList(cmds.polyListComponentConversion(vert, toEdge=True ))
    return [x.split('[')[1].split(']')[0] for x in adges2 if x in adges and x!=adges[0]]

 
