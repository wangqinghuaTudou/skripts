
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maya.cmds as cmds
from CharacterNames import CharacterNames as chn
from an_classNames import AnNames
from an_classControllers import AnControllers as ctrl
from  an_Procedures.rivet import  rivet
from  an_Procedures.utilities import  an_convertSliceToList, an_distans, an_turnBasedUi


'''
             ribbon

    ikPointRigSys()         
    sortPolyFaceseLine()     
    nurbsPlaneOnJnt() 
    rivetJntOnPlane()        
    ribonUi()
'''


def ikPointRigSys(pfx='roup', jntNum=12, ctSize=1):
    
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
 
def nurbsPlaneOnJnt(jntList, pfx='', geo = 'nurbs'):
    if not pfx: pfx=chn(jntList[0]).sfxMinus()
    prWeight = an_distans (jntList[0], jntList[-1])/40 
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
    for e1, e2 in sortPolyFaceseLine(polySkin):
        rvt = rivet(polySkin, [e1, e2], out="joint")
        rivetJnt.append(rvt)
    rivetGrp = cmds.group(rivetJnt, n=pfx+'Rivet_grp')
    return rivetJnt, polySkin

def sortPolyFaceseLine(geo):
    riv_edges =[geo+'.e[1]', ]
    for i in range(cmds.polyEvaluate(geo, f=True )):
        if i==0:
            vert= an_convertSliceToList(cmds.polyListComponentConversion(riv_edges[-1] , toVertex=True )) 
        else:
            vert= an_convertSliceToList(cmds.polyListComponentConversion(riv_edges[-2:] , toVertex=True ))
        r_edges = [x for x in  an_convertSliceToList(cmds.polyListComponentConversion(vert, toEdge=True, border=True ))  if not x in riv_edges] 
        riv_edges += r_edges
    n_list = [x.split('[')[1].split(']')[0] for x in  riv_edges[1:]] 
    return  [ [n_list[x], n_list[x+1]]  for x in  range(0, len(n_list), 2)]
    
def ribonUi(mode = 'Ui'):
    if mode =='Ui':
        leyaut =  an_turnBasedUi('roup', title ='Ribbon creater',  stepsLabel =['Select the required joints and click create'], stepNum=False)
        cmds.setParent(leyaut)
        cmds.columnLayout( )
        cmds.textFieldGrp('pfxTFG', label='Prefix', text='roup' )
        cmds.intSliderGrp('jNumISG',  field=True, label='Joint number', minValue=1, maxValue=30, fieldMinValue=1, fieldMaxValue=2000, value=10 )  
        cmds.floatSliderGrp('cSizeFSG',  label='Controllers size', field=True, minValue=0.5, maxValue=3.0, fieldMinValue=0.0, fieldMaxValue=100.0, value=1 )   
        cmds.button(  l='Create',  width=385,  command='ribonUi("Create")')
        cmds.separator(height=1, style='none')
    else: #comand mod
        tx = cmds.textFieldGrp('pfxTFG', q=1, text=1 )
        jnts = cmds.intSliderGrp('jNumISG', q=1, v=1 )
        ctSz = cmds.floatSliderGrp('cSizeFSG', q=1, v=1 )
        ikPointRigSys(tx, jnts+1, ctSz) 

 
  

 

 
 
 
 
 
 
 
 
