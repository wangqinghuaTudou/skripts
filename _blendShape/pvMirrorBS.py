"""
-------------------------------------------------------------------------
       Script: pvMirrorBS.py
       Author: Pavel Volokushin
        email: p.volokushin@gmail.com
Creation date: 26.09.2014
        Usage: pvMirrorBS()
  Description: This script makes mirrored copy of the selected blendshape
               target, place it to opposite side and rename it form left
               side to the right.
-------------------------------------------------------------------------
"""

import maya.cmds as mc
import maya.mel as mm

def pvMirrorBS():
    if (mc.window ('mirrorBlendshape_ui', exists = True)):
        mc.deleteUI ('mirrorBlendshape_ui')
    mc.window ('mirrorBlendshape_ui', \
               resizeToFitChildren=True, \
               sizeable=False, \
               title='Mirror Blendshape')
    mc.columnLayout(adjustableColumn=True)
    # text field for base
    mc.textFieldButtonGrp('baseMirrBsTgbf', \
                          label='Base Geometry:', \
                          buttonLabel='Assign', \
                          buttonCommand='mc.textFieldButtonGrp("baseMirrBsTgbf", \
                          edit=True, text=mc.ls(sl=True)[0])')
    # text field for target
    mc.textFieldButtonGrp('targetMirrBsTgbf', \
                          label='Target Geometry:', \
                          buttonLabel='Assign', \
                          buttonCommand='mc.textFieldButtonGrp("targetMirrBsTgbf", \
                          edit=True, text=mc.ls(sl=True)[0])')
    mc.separator (height=5, style='in')
    mc.text('Max Distance:', align='left')
    # float field for max distance value
    mc.floatField('pvMaxDistFf', width=80, value = 0.01, precision=2)
    mc.separator (height=5, style='in')
    # button for running main script
    mc.button (label='Run', align='center', c='pvMirrorBSmain ()')
    mc.showWindow ('mirrorBlendshape_ui')

def pvMirrorBSmain ():
    mc.select(clear=True)
    # getting base and target names
    base = mc.textFieldButtonGrp('baseMirrBsTgbf', query=True, text=True)
    target = mc.textFieldButtonGrp('targetMirrBsTgbf', query=True, text=True)
    # getting max distance value
    maxDist = mc.floatField('pvMaxDistFf', query=True, value=True)
    # getting target's position
    tx = mc.getAttr('%s.tx'%target)
    ty = mc.getAttr('%s.ty'%target)
    tz = mc.getAttr('%s.tz'%target)
    # create duplicate for blendshapes
    dupBaseBS = mc.duplicate(base, returnRootsOnly=True)[0]
    # create duplicate for wrap deformer
    dupBaseWrap = mc.duplicate(base, returnRootsOnly=True)[0]
    # create blendshape from target to base duplicate
    blendSh = mc.blendShape(target, dupBaseBS, topologyCheck=False)[0]
    # set scale x of base duplicate to -1
    attrList = mc.listAttr(dupBaseBS, k=True)
    if attrList:
        for attr in attrList:
            mc.setAttr('%s.%s'%(dupBaseBS, attr), lock=False)
    mc.setAttr('%s.sx'%dupBaseBS, -1)
    # selecting wrap duplicate and blendshape duplicate
    mc.select(dupBaseWrap, dupBaseBS, r=True)
    # create and settings wrap deformer
    wrapDef = mm.eval("doWrapArgList \"6\" { \"1\",\"0\",\""+str(0.01)+"\", \"2\", \"0\", \"0\", \"0\" };")[0]
    #wrapDef = mc.deformer(dupBaseWrap, type='wrap')[0]
    mc.setAttr('%s.autoWeightThreshold'%wrapDef, 0)
    mc.setAttr('%s.exclusiveBind'%wrapDef, 0)
    mc.setAttr('%s.falloffMode'%wrapDef, 0)
    mc.setAttr('%s.maxDistance'%wrapDef, maxDist)
    mc.setAttr('%s.weightThreshold'%wrapDef, 0)
    # create opposite target
    mc.setAttr('%s.%s'%(blendSh, target), 1)
    oppTarget = mc.duplicate(dupBaseWrap, returnRootsOnly=True)[0]
    # delete unnecessary duplicates
    mc.delete(dupBaseBS, dupBaseWrap)
    # rename opposite target
    oppTarget = mc.rename(oppTarget, target.replace('l_','r_'))
    attrList = mc.listAttr(oppTarget, k=True)
    if attrList:
        for attr in attrList:
            mc.setAttr('%s.%s'%(oppTarget, attr), lock=False)
    # move opposite target to opposite side
    mc.setAttr('%s.tx'%oppTarget, -tx)
    mc.setAttr('%s.ty'%oppTarget, ty)
    mc.setAttr('%s.tz'%oppTarget, tz)
    # unparent opposite target to the world
    if mc.listRelatives(oppTarget, parent=True):
        mc.parent(oppTarget, world=True)
    mc.select(oppTarget, replace=True)
    mc.sets(e=True, forceElement='initialShadingGroup')
    mc.select(clear=True)

# pvMirrorBS()