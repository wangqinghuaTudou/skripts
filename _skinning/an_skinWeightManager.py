# 22.11.2021 new functions flood_shell
# 02.09.2020 new functions copyWeightsFromObjects
# 28.04.2020 new functions used
# 11.12.2019 add buttons
# 10.12.2019 add selektSkinJnts proc
# 18.07.2019 add copy proc

from an_Procedures.utilities import an_turnBasedUi, an_convertSliceToList
from an_skinProcedures import *
import maya.cmds as cmds
import maya.mel as mm


def an_skinWeightManager():
    leauts = an_turnBasedUi('skn',
                            title='Skin weight manager  v 2.00',
                            stepNum=False,
                            stepsLabel=["Default lib path:",
                                        "Save/Load skining:",
                                        "Copy weights to vertex",
                                        "Copy weights",
                                        "Other tools"])

    # Default lib path
    vEnv = mm.eval("getenv (\"HOME\")")
    cmds.textField("PathTF", tx=vEnv, p=leauts[0])
    cmds.button(l="Add path", c="an_addPath()", p=leauts[0])

    # Save/Load skining
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 213), (2, 214)], columnSpacing=[(2, 2), (3, 2)],
                         p=leauts[1], rowSpacing=[(2, 2), (3, 2)], )
    cmds.button(label='Load skin weight', command="loadSkin()")
    cmds.button(label='Save skin weight', command='saveSkin()')

    # Copy weights to vertex
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 100), (2, 214), (3, 113)], columnSpacing=[(2, 2), (3, 2)],
                         p=leauts[2])
    cmds.text('Copy from:')
    TF = cmds.textField("copTF")
    com = "cmds.textField ('" + TF + "', e=True, tx= cmds.ls (sl=True)[0]);"
    cmds.button('adSel', label='add sel', command=com)
    cmds.setParent("..")
    cmds.button(label='Copy weights to vertex', command='copySkinToVertex()')

    # Copy weights
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 142), (2, 142), (3, 142)],
                         columnSpacing=[(2, 2), (3, 2), (3, 2)], p=leauts[3], rowSpacing=[(2, 2), (3, 2)])
    cmds.button(label='Copy and mirrow weights ', command="copyAndMirrowWeights()")
    cmds.button(label='Copy from several', command="copyWeightsFromObjects()")
    cmds.button(label='Copy to several', command="copySkinToListObjects()")
    cmds.setParent("..")

    # Other tools
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 142), (2, 142), (3, 142)],
                         columnSpacing=[(2, 2), (3, 2), (3, 2)], p=leauts[4], rowSpacing=[(2, 2), (3, 2)])
    cmds.button(label='Flood shell', command="flood_shell()")
    cmds.button(label='Select skin joints', command="selektSkinJnts()")
    cmds.button(label='Reskin geometry', command='reskin()')

    cmds.canvas(h=5)


def __getJntAndVertexes():  # return joint an vertexes list
    sel = cmds.ls(sl=True)
    joint = [x for x in sel if cmds.nodeType(x) == "joint"][0]
    selFaces = cmds.filterExpand(sm=34)  # get face if it exist
    if selFaces:
        sel_vertexees = an_convertSliceToList(cmds.polyListComponentConversion(selFaces, tv=True))
    else:
        sel_vertexees = [x for x in sel if not cmds.nodeType(x) == "joint"]
    vertexees = []
    while sel_vertexees:
        node = sel_vertexees.pop()
        vertex = an_convertSliceToList([node])
        vertexees += vertex
    return joint, vertexees


def flood_shell():
    mm.eval('polyConvertToShell;')
    joint, vertexees = __getJntAndVertexes()

    geo = vertexees[0].split(".vtx")[0]
    weight = getSkin(geo)
    pointNumber = len(weight[weight.keys()[0]])
    if not joint in weight.keys():
        weight[joint] = [0 for x in range(pointNumber)]
    vertex_indexes = [int(x.split(".vtx[")[-1][:-1]) for x in vertexees]
    for jnt in weight.keys():
        if jnt == joint:
            for i in vertex_indexes:
                weight[jnt][i] = 1
        else:
            for i in vertex_indexes:
                weight[jnt][i] = 0
    setSkin(geo, weight)


def an_addPath():
    vPathName = cmds.fileDialog2(fileMode=2, caption="Add path")
    cmds.textField("PathTF", e=True, tx=vPathName[0])


def loadSkin(recordNod=''):
    vDir = cmds.textField("PathTF", q=True, tx=True)
    dataList = an_saveLoadData(obgect=recordNod, vDir=vDir)[0]
    for geo in dataList.keys(): setSkin(geo, dataList[geo])


def saveSkin(recordNod=''):
    listGeo = cmds.ls(sl=True)
    dataList = {}
    for geo in listGeo:   dataList[geo] = getSkin(geo)
    vDir = cmds.textField("PathTF", q=True, tx=True)
    an_saveLoadData(data=[dataList, ], obgect=recordNod, delAttr=False, vDir=vDir)


def selektSkinJnts():
    skinClusterName = cmds.ls(cmds.listHistory(cmds.ls(sl=True)), type='skinCluster')[0]
    jointName = cmds.ls(cmds.listHistory(skinClusterName, levels=1), type='transform')
    cmds.select(jointName)
    return jointName


def reskin():
    objectName = cmds.ls(sl=True)[0]
    weightList = getSkin(objectName)
    skinClusterName = cmds.ls(cmds.listHistory(objectName, pdo=1), type='skinCluster')[0]  ### if claster sel
    cmds.skinCluster(skinClusterName, e=True, ub=True)
    setSkin(objectName, weightList)


def copySkinToListObjects():
    lst = cmds.ls(sl=True)
    for geo in lst[1:]:  copySkin(lst[0], geo)


def copySkinToVertex():
    destVert = an_convertSliceToList(cmds.ls(sl=True))
    sourceObj = cmds.textField("copTF", q=1, tx=1)
    copySkinToSelVertex(sourceObj, destVert)


def copyWeightsFromObjects():
    sGeo = cmds.ls(sl=True)[:-1]
    geo = cmds.ls(sl=True)[-1]

    if cmds.ls(cmds.listHistory(geo), type='skinCluster'):
        skCluster = cmds.ls(cmds.listHistory(geo), type='skinCluster')[0]
        cmds.skinCluster(skCluster, e=True, ub=True)

    jntList = []
    for each in sGeo:
        skinCluster = cmds.ls(cmds.listHistory(each), type='skinCluster')[0]
        jnts = cmds.ls(cmds.listHistory(skinCluster, levels=1), type='transform')  ###   jnt
        jntList += jnts

    skCluster = cmds.skinCluster(jntList, geo, tsb=True, normalizeWeights=True)[0]  # skinning
    cmds.select(sGeo + [geo])
    cmds.copySkinWeights(noMirror=True, surfaceAssociation='closestPoint', influenceAssociation='oneToOne')


if __name__ == "__main__":
    an_skinWeightManager()
