
geo = cmds.ls(sl=True)[0]
tGro = 'nogaExoskeletaPravaya_v007:'+geo
copySkin(geo, tGro )
cmds.select(geo)




geo = cmds.ls(sl=True)[0]
deformerNod = cmds.listHistory (geo, levels=1)[1]

if cmds.nodeType(deformerNod) == 'melnitsaWrap': 
    influensShape=cmds.connectionInfo(deformerNod+'.obstacleMesh', sourceFromDestination =True).split('.')[0]
    defGeo = cmds.listRelatives(influensShape, p=True)[0]            

cageShape = cmds.listRelatives( defGeo, s=True )[0]
cmds.select('nogaExoskeletaPravaya_v007:'+geo)
deform = cmds. deformer (type='melnitsaWrap')[0]
cmds. connectAttr (cageShape+'.worldMesh[0]', deform+'.obstacleMesh')

cmds.select(geo)