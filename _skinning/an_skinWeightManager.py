# 28.04.2020 new functions used
# 11.12.2019 add buttons
# 10.12.2019 add selektSkinJnts proc
# 18.07.2019 add copy proc
 
from an_Procedures.utilities import  *
from an_skinProcedures import  *
import maya.cmds as cmds
import maya.mel as mm

def an_skinWeightManager():  
    leauts = an_turnBasedUi('skn', title ='Skin weight manager  v 2.00',  stepsLabel =["Default lib path:", "Save/Load skining:", "Copy weights to vertex", "Copy weights"  ])
    
    vEnv = mm.eval("getenv (\"HOME\")")
    cmds.textField("PathTF", tx=vEnv, p=leauts[0])
    cmds.button (l="Add path", c="an_addPath()"  ,p=leauts[0])
  
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 213), (2, 214)], columnSpacing=[(2,2),(3,2)], p=leauts[1], rowSpacing=[(2,2),(3,2)], ) 
    cmds.button( label='Load skin weight', command= "loadSkin()" )
    cmds.button( label='Save skin weight', command= 'saveSkin()')
    cmds.button( label='Select skin joints', command= "selektSkinJnts()" ) 
    cmds.button( label='Reskin geometry', command= 'reskin()' )

    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 214), (3, 113)], columnSpacing=[(2,2),(3,2)], p=leauts[2] )
    cmds.text('Copy from:')
    TF = cmds.textField("copTF" )
    com = "cmds.textField ('"+TF+"', e=True, tx= cmds.ls (sl=True)[0]);"
    cmds.button('adSel', label='add sel', command= com)
    cmds.setParent ("..")
    cmds.button( label='Copy weights to vertex', command= 'copySkinToVertex()')

    cmds.button( label='Copy weights', command= "copySkinToListObjects()", p=leauts[3])
    cmds.setParent ("..")
    cmds.canvas(h=5)

def an_addPath ():
    vPathName = cmds.fileDialog2(fileMode=2, caption="Add path")
    cmds.textField("PathTF", e=True, tx=vPathName[0])

def loadSkin( recordNod='' ):
    vDir = cmds.textField("PathTF", q=True, tx=True)
    dataList = an_saveLoadData( obgect=recordNod, vDir=vDir)[0]
    for geo in dataList.keys(): setSkin (geo,  dataList[geo])

def saveSkin( recordNod='' ):
    listGeo = cmds.ls (sl=True)
    dataList ={}
    for geo in  listGeo:   dataList[geo]= getSkin(geo)
    vDir = cmds.textField("PathTF", q=True, tx=True)
    an_saveLoadData(data=[dataList,], obgect=recordNod, delAttr = False, vDir=vDir)

def selektSkinJnts():
    skinClusterName = cmds.ls (cmds.listHistory (cmds.ls (sl=True) ), type='skinCluster')[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')
    cmds.select(jointName)
    return jointName
    
def reskin():
    objectName = cmds.ls (sl=True)[0]
    weightList = getSkin (objectName)
    skinClusterName =  cmds.ls (cmds.listHistory (objectName, pdo=1), type='skinCluster')[0]    ### if claster sel
    cmds.skinCluster(skinClusterName,   e=True, ub=True )
    setSkin ( objectName,  weightList)
    
def copySkinToListObjects():
    lst= cmds.ls (sl=True)
    for geo in lst[1:]:  copySkin( lst[0] ,geo)

def copySkinToVertex():
    destVert= an_convertSliceToList(cmds.ls (sl=True))
    sourceObj = cmds.textField("copTF", q=1, tx=1 )
    copySkinToSelVertex(sourceObj, destVert)








    


    