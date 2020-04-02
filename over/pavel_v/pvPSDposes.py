import maya.cmds as mc
from pvDuplicatePose import *


alembicPrefix = 'alembic_'
geoSuffix = '_geo'
baseGrp = 'BSclothBase_grp'
deformGrp = 'BSclothDeform_grp'
baseName = 'DefaultBase'
deformName = 'DefaultDeform'

clothGeoList = ['shirt'] #, 'waistcoatBack', 'l_waistcoat', 'r_waistcoat']
#bodyPartsList = ['spine', 'clavicles', 'arms']

keyframesList = [{40:'BSspineFrontBase_geo', \
                  120:'BSspineBackBase_geo', \
                  200:'BSspineBendRightBase_geo', \
                  280:'BSspineBendLeftBase_geo', \
                  360:'BSspineTwistLeftBase_geo', \
                  440:'BSspineTwistRightBase_geo'}, \
                 {520:'BSclaviclesFrontBase_geo', \
                  580:'BSclaviclesBackBase_geo', \
                  660:'BSclaviclesUpBase_geo', \
                  740:'BSclaviclesDownBase_geo'}, \
                 {820:'BSarmsFrontBase_geo', \
                  900:'BSarmsBackBase_geo', \
                  980:'BSarmsUpBase_geo', \
                  1060:'BSarmsDownBase_geo'}]

for clothGeo in clothGeoList:

    clothGeoName = clothGeo + geoSuffix
    baseGrpName = clothGeo + baseGrp
    deformGrpName = clothGeo + deformGrp
    baseClothName = clothGeo + baseName + geoSuffix
    deformClothName = clothGeo + deformName + geoSuffix

    isBaseGrpExists = mc.objExists(baseGrpName)
    if not isBaseGrpExists:
        mc.group(name=baseGrpName, empty=True, parent='root')

    isDeformGrpExists = mc.objExists(deformGrpName)
    if not isDeformGrpExists:
        mc.group(name=deformGrpName, empty=True, parent='root')

    children = mc.listRelatives(baseGrpName, children=True)
    if children:
        mc.delete(children)

    children = mc.listRelatives(deformGrpName, children=True)
    if children:
        mc.delete(children)

    mc.currentTime(1)

    dup = pvDuplicatePose(clothGeoName)
    mc.rename(dup, baseClothName)
    mc.parent(baseClothName, baseGrpName)
    mc.setAttr(baseClothName + '.v', 0)

    dup = pvDuplicatePose(alembicPrefix + clothGeoName)
    mc.rename(dup, deformClothName)
    mc.parent(deformClothName, deformGrpName)
    mc.setAttr(deformClothName + '.v', 0)

    psdName = ''
    hist = mc.listHistory(clothGeoName, pdo=True)
    if hist:
        psdName = mc.ls(hist, type='melnitsaPoseSpaceDeformer')[0]
    if not psdName:
        om.MGlobal.displayInfo('Must exists PSD in history.')
        break
    else:
        try:
            shapes = mc.listRelatives(baseClothName, shapes=True)
            if not shapes:
                om.MGlobal.displayInfo('Cloth geometry must has any shape(s).')
                break
            else:
                mainObjectShape = shapes[0]
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[0].targetMeshBase[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[1].targetMeshBase[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[2].targetMeshBase[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[3].targetMeshBase[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[4].targetMeshBase[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[0].targetMeshSculpt[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[1].targetMeshSculpt[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[2].targetMeshSculpt[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[3].targetMeshSculpt[0]', force=True)
                mc.connectAttr(mainObjectShape + '.worldMesh[0]', psdName + '.zoneList[4].targetMeshSculpt[0]', force=True)
        except:
            raise

    for keyframes in keyframesList:
        for i, kf in enumerate(keyframes):

            mc.currentTime(kf)

            baseClothName = clothGeo + keyframes.get(kf)
            dup = pvDuplicatePose(clothGeoName)
            mc.rename(dup, baseClothName)
            mc.parent(baseClothName, baseGrpName)
            mc.setAttr(baseClothName + '.v', 0)

            deformClothName = baseClothName.replace('Base', 'Deform')
            dup = pvDuplicatePose(alembicPrefix + clothGeoName)
            mc.rename(dup, deformClothName)
            mc.parent(deformClothName, deformGrpName)
            mc.setAttr(deformClothName + '.v', 0)

            baseShape = mc.listRelatives(baseClothName, shapes=True)[0]
            deformShape = mc.listRelatives(deformClothName, shapes=True)[0]

            if 'spine' in baseClothName:
                mc.connectAttr(baseShape + '.worldMesh[0]', psdName + '.zoneList[0].targetMeshBase[%s]'%(i + 1))
                mc.connectAttr(deformShape + '.worldMesh[0]', psdName + '.zoneList[0].targetMeshSculpt[%s]'%(i + 1))
            elif 'arms' in baseClothName:
                mc.connectAttr(baseShape + '.worldMesh[0]', psdName + '.zoneList[3].targetMeshBase[%s]'%(i + 1))
                mc.connectAttr(deformShape + '.worldMesh[0]', psdName + '.zoneList[3].targetMeshSculpt[%s]'%(i + 1))
                mc.connectAttr(baseShape + '.worldMesh[0]', psdName + '.zoneList[4].targetMeshBase[%s]'%(i + 1))
                mc.connectAttr(deformShape + '.worldMesh[0]', psdName + '.zoneList[4].targetMeshSculpt[%s]'%(i + 1))
            elif 'clavicles' in baseClothName:
                mc.connectAttr(baseShape + '.worldMesh[0]', psdName + '.zoneList[1].targetMeshBase[%s]'%(i + 1))
                mc.connectAttr(deformShape + '.worldMesh[0]', psdName + '.zoneList[1].targetMeshSculpt[%s]'%(i + 1))
                mc.connectAttr(baseShape + '.worldMesh[0]', psdName + '.zoneList[2].targetMeshBase[%s]'%(i + 1))
                mc.connectAttr(deformShape + '.worldMesh[0]', psdName + '.zoneList[2].targetMeshSculpt[%s]'%(i + 1))

mc.currentTime(1)