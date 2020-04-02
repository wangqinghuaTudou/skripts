import maya.cmds as mc

def pvCreateCorrBS():
    if (mc.window ('pvRigBS_ui', exists = True)):
        mc.deleteUI ('pvRigBS_ui')
    mc.window ('pvRigBS_ui', \
               width=200, \
               height=40, \
               resizeToFitChildren=True, \
               sizeable=False, \
               title='Create Corr BS')
    mc.columnLayout(adjustableColumn=True)
    mc.textFieldButtonGrp('baseTgbf', label='Base:', buttonLabel='Assign', buttonCommand='mc.textFieldButtonGrp("baseTgbf", edit=True, text=mc.ls(sl=True)[0])')
    mc.textFieldButtonGrp('corrTgbf', label='Corrective:', buttonLabel='Assign', buttonCommand='mc.textFieldButtonGrp("corrTgbf", edit=True, text=mc.ls(sl=True)[0])')
    mc.radioButtonGrp('parllRbg', label='Parallel: ', labelArray2=['Off', 'On'], numberOfRadioButtons=2, select=2)
    mc.radioButtonGrp('placeRbg', label='lacement: ', labelArray3=['Base', 'Corr', 'Mirror'], numberOfRadioButtons=3, select=2)
    mc.button (label='Make Corrective', command='pvCreateCorrBSmain()')
    mc.showWindow ('pvRigBS_ui')

def pvCreateCorrBSmain():
    mc.select(clear=True)
    base = mc.textFieldButtonGrp('baseTgbf', query=True, text=True)
    corr = mc.textFieldButtonGrp('corrTgbf', query=True, text=True)
    parll = mc.radioButtonGrp('parllRbg', query=True, select=True)
    place = mc.radioButtonGrp('placeRbg', query=True, select=True)
    if place == 1:
        tx = mc.getAttr('%s.tx'%base)
        ty = mc.getAttr('%s.ty'%base)
        tz = mc.getAttr('%s.tz'%base)
    elif place == 2:
        tx = mc.getAttr('%s.tx'%corr)
        ty = mc.getAttr('%s.ty'%corr)
        tz = mc.getAttr('%s.tz'%corr)
    else:
        tx = -mc.getAttr('%s.tx'%base)
        ty = mc.getAttr('%s.ty'%base)
        tz = mc.getAttr('%s.tz'%base)
    deformers = mc.listHistory(base, pruneDagObjects=1)
    dupBase = mc.duplicate(base, returnRootsOnly=True)[0]
    if mc.listRelatives(dupBase, parent=True):
        dupBase = mc.parent(dupBase, world=True)[0]
    mc.blendShape(dupBase, corr, base, name='temp_bs', parallel=parll-1, topologyCheck=False)
    mc.setAttr('temp_bs.%s'%dupBase, -1)
    mc.setAttr('temp_bs.%s'%corr, 1)
    if deformers:
        for each in deformers:
            if mc.attributeQuery('envelope', node=each, exists=True):
                mc.setAttr('%s.envelope'%each, 0)
    corrCalc = mc.duplicate(base, returnRootsOnly=True, name=corr.replace('_geo','Corr_geo'))[0]
    if mc.listRelatives(corrCalc, parent=True):
        corrCalc = mc.parent(corrCalc, world=True)[0]
    if deformers:
        for each in deformers:
            if mc.attributeQuery('envelope', node=each, exists=True):
                mc.setAttr('%s.envelope'%each, 1)
    currDefList = mc.ls(mc.listHistory(base, pruneDagObjects=1), type='blendShape')
    if currDefList:
        for curr in currDefList:
            if curr not in deformers and mc.objExists(curr):
                mc.delete(curr)
    mc.delete(dupBase)
    mc.setAttr('%s.tx'%corrCalc, tx)
    mc.setAttr('%s.ty'%corrCalc, ty)
    mc.setAttr('%s.tz'%corrCalc, tz)
    mc.select(corrCalc, replace=True)
    mc.sets(e=True, forceElement='initialShadingGroup')
    mc.select(clear=True)

# pvCreateCorrBS()