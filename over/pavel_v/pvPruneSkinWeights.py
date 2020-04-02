"""
-------------------------------------------------------------------------
       Script: pvPruneSkinWeights.py
       Author: Pavel Volokushin
        email: p.volokushin@gmail.com
Creation date: 13.10.2014
        Usage: pvPruneSkinWeights()
  Description: This script prune skin weights less than 0.099 on selected
               object. And remove unused influences after that.
       Needed: Two addition procedures from pvProcedures.py 
               pvGetSkinCluster()
               pvRemoveUnusedInfl(skin)
-------------------------------------------------------------------------
"""

import maya.cmds as mc
import pvProcedures as pvp

def pvPruneSkinWeights():
    if mc.window('pvPruneSkinWeights_ui', exists=True):
        mc.deleteUI('pvPruneSkinWeights_ui')
    mc.window('pvPruneSkinWeights_ui', \
              sizeable=False, \
              width=150, \
              height=100, \
              title='Rename Objects')
    mc.columnLayout(adjustableColumn=True)
    mc.floatField('pvPruneValFf', minValue=0, maxValue=1, width=80, value = 0.0099, precision=4)
    mc.button(label='Run', command='pvPruneSkinWeightsMain()')
    mc.showWindow('pvPruneSkinWeights_ui')

def pvPruneSkinWeightsMain(*args):
    # if haven't args try to check current selection 
    if not args:
        args = mc.ls(selection=True)
    # if nothing selected then warning and return 
    if not args:
        mc.warning('At least one object must be selected.')
        return
    pruneVal = mc.floatField('pvPruneValFf', query=True, value=True)
    for each in args:
        # getting skin cluster name 
        skin = pvp.pvGetSkinCluster(mc.ls(sl=True))
        # getting influences names
        infls = mc.skinCluster(skin, query=True, influence=True)
        for inf in infls:
            # setting lock weight attribute is off on each influence
            mc.setAttr('%s.liw'%inf, 0)
        # prune small weights
        mc.skinPercent(skin, each, pruneWeights=pruneVal )
        # remove unused influences 
        pvp.pvRemoveUnusedInfl(skin)

# pvPruneSkinWeights()