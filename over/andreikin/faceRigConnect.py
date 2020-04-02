import maya.cmds as cmds  
from an_classNames import AnNames as CharacterNames 

geoList = cmds.ls(sl=1)
grGeo = 'faceGeo_grp'
if not cmds.objExists(grGeo): cmds.group( n= 'faceGeo_grp' , em=True )

for geo in geoList: 
    rGeo = CharacterNames(geo).sfxMinus()+"_FRgeo"
    cmds.rename(geo, rGeo)
    duplikat = cmds.duplicate (rGeo, n=geo )[0]
    cmds.parent(duplikat,  grGeo)
    connectAttr (rGeo+'.outMesh', geo+'.outMesh')