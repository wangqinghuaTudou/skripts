import maya.cmds as mc

upWireCurve = 'up_lipPolyEdge_crv'
loWireCurve = 'lo_lipPolyEdge_crv'
obj = mc.ls(sl=True)[0]
shape = mc.listRelatives(obj, shapes=True)[0]
history = mc.listHistory(obj, pruneDagObjects=True)
skinCl = mc.ls(history, type='skinCluster')[0]
loWire, upWire = mc.ls(history, type='wire')
vtxIndexes = mc.getAttr(shape + '.vrts', multiIndices=True)
upWireWeights = {}
loWireWeights = {}
for i in vtxIndexes:
    upWireWeights[obj + '.vtx[%s]'%i] = mc.percent(upWire, obj + '.vtx[%s]'%i, query=True, value=True)[0]
    loWireWeights[obj + '.vtx[%s]'%i] = mc.percent(loWire, obj + '.vtx[%s]'%i, query=True, value=True)[0]

for i in vtxIndexes:
    mc.skinPercent(skinCl, obj + '.vtx[%s]'%i, transformValue=[(upWireCurve, upWireWeights[obj + '.vtx[%s]'%i])])
    mc.skinPercent(skinCl, obj + '.vtx[%s]'%i, transformValue=[(loWireCurve, loWireWeights[obj + '.vtx[%s]'%i])])