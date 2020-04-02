"""
-------------------------------------------------------------------------
       Script: pvCopySkinToOpposite.py
       Author: Pavel Volokushin
        email: p.volokushin@gmail.com
Creation date: 13.10.2014
        Usage: pvCopySkinToOpposite()
  Description: This script create skinCluster to opposite side geometry if
               it exists. And copy skin weights on it. 
       Needed: Two addition procedures from pvProcedures.py 
               pvGetSkinCluster()
               pvRemoveUnusedInfl(skinClusterName)
-------------------------------------------------------------------------
"""

import maya.cmds as mc
import pvProcedures as pvp

def pvCopySkinToOpposite(obj):
    # getting main prefix 
    mainPref = obj[:2]
    # set the opposite side prefix
    if mainPref == 'l_':
        oppPref = mainPref.replace('l_','r_')
    elif mainPref == 'r_':
        oppPref = mainPref.replace('r_','l_')
    else:
        oppPref = mainPref
    # getting opposite geometry's name
    opp = oppPref + obj[2:]
    # getting skinCluster name on main object 
    skin = pvp.pvGetSkinCluster(obj)
    # getting list of influences and other attribute's values from skinCluster 
    infls = mc.skinCluster(skin, query=True, influence=True)
    jnts = mc.ls(infls, type='joint')
    nurbs = list(set(infls).difference(jnts))   
    maxInfs = mc.skinCluster(skin, query=True, maximumInfluences=True)
    # getting list of influences names for opposite skinCluster
    rJnts = [j.replace(mainPref, oppPref) if mainPref in j else j for j in jnts]
    rNurbs = [n.replace(mainPref, oppPref) if mainPref in n else n for n in nurbs]
    # create opposite skinCluster
    oppSkin = mc.skinCluster(opp, rJnts, toSelectedBones=True, \
                             useGeometry=True, \
                             dropoffRate=4, \
                             polySmoothness=False, \
                             nurbsSamples=25, \
                             removeUnusedInfluence=False, \
                             maximumInfluences=maxInfs, \
                             obeyMaxInfluences=False, \
                             normalizeWeights=True)[0]
    # adding nurbs influences to opposite skinCluster
    for n in rNurbs:
        mc.select (opp, replace=True)
        mc.select (n, add=True)
        mc.skinCluster(oppSkin, edit=True, addInfluence=n, useGeometry=True, polySmoothness=0.0, nurbsSamples=25)
    # settinguseComponents attribute if it needs
    if mc.getAttr('%s.useComponents'%skin): mc.setAttr('%s.useComponents'%oppSkin, 1)
    # mirror skin weights from main skinCluster to opposite
    mc.copySkinWeights (obj, opp, \
                     sourceSkin=skin, \
                     destinationSkin=oppSkin, \
                     mirrorMode='YZ', \
                     surfaceAssociation='closestPoint', \
                     influenceAssociation='oneToOne')
    # remove unused influences on opposite skinCluster
    pvp.pvRemoveUnusedInfl(oppSkin)
    mc.select(clear=True)
    
# pvCopySkinToOpposite(mc.ls(selection=True)[0])