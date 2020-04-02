
# 11.12.2019 add buttons
# 10.12.2019 add selektSkinJnts proc
# 18.07.2019 add copy proc
 
from an_skinProcedures import *
from  anProcedures import  *
from an_classSkin import AnSkinSys
import maya.cmds as cmds
import maya.mel as mm


def an_skinWeightManager():  
    leauts = an_turnBasedUi('skn', title ='Skin weight manager  v 2.00',  stepsLabel =["Default lib path:", "Save/Load skining:", "Copy weights to vertex", "Copy weights"  ])
    
    vEnv = mm.eval("getenv (\"HOME\")")
    cmds.textField("PathTF", tx=vEnv, p=leauts[0])
    cmds.button (l="Add path", c="an_addPath()"  ,p=leauts[0])
  
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 213), (2, 214)], columnSpacing=[(2,2),(3,2)], p=leauts[1], rowSpacing=[(2,2),(3,2)], ) 
    cmds.button( label='Load skin weight', command= "restorSkin()" )
    cmds.button( label='Save skin weight', command= 'recordSkin()')
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
    skinToolsUI()
    
    
    
def copySkinToListObjects():
    lst= cmds.ls (sl=True)
    for geo in lst[1:]:  AnSkinSys('').copySkin( lst[0] ,geo)
    
    
def skinToolsUI():
    colNum = 5
    cmds.rowColumnLayout("STUI", nc=10, columnWidth=[(x+1, 33) for x in range(colNum)])
    buttList = (("paintSkinWeights.png", "ArtPaintSkinWeightsTool"), 
                ("smoothSkin.png", "SmoothBindSkin"), 
                ("detachSkin.png", "DetachSkin"), 
                ("addWrapInfluence.png", "AddInfluence"), 
                ("removeWrapInfluence.png", "RemoveInfluence"),
                ("menuIconSkinning.png", "br_smoothSkinClusterWeightPaint"), 
                ("mirrorSkinWeight.png", "MirrorSkinWeights"))
    for img, com  in buttList:
        cmds.shelfButton (enableCommandRepeat=1, 
                            label=img ,
                            image=img ,
                            image1=img, 
                            command=com ,
                            sourceType="mel" ,)

#an_skinWeightManager()

def copySkinToVertex():
    destVert= an_convertPointsNames(cmds.ls (sl=True))
    sourceObj = cmds.textField("copTF", q=1, tx=1 )
    AnSkinSys('').copySkinToSelectionsVertex(sourceObj, destVert)

def reskin():
    objectName = cmds.ls (sl=True)[0]
    weightList = getSkinJntAndWeight(objectName)
    skinClusterName =  cmds.ls (cmds.listHistory (objectName, pdo=1), type='skinCluster')[0]    ### if claster sel
    cmds.skinCluster(skinClusterName,   e=True, ub=True )
    setSkinAndWeight ( objectName,  weightList)

def recordSkin( recordNod='' ):
    listGeo = cmds.ls (sl=True)
    dataList ={}
    for geo in  listGeo: 
        #dataList[geo]= getSkinJntAndWeight(geo)
        dataList[geo]=AnSkinSys(geo).getSkinWeights()
    vDir = cmds.textField("PathTF", q=True, tx=True)
    an_saveLoadData(data=[dataList,], obgect=recordNod, delAttr = False, vDir=vDir)


def restorSkin( recordNod='' ):
    vDir = cmds.textField("PathTF", q=True, tx=True)
    dataList = an_saveLoadData( obgect=recordNod, vDir=vDir)[0]
    for geo in dataList.keys(): setSkinAndWeight ( geo,  dataList[geo])

def an_addPath ():
    vPathName = cmds.fileDialog2(fileMode=2, caption="Add path")
    cmds.textField("PathTF", e=True, tx=vPathName[0])
    
def selektSkinJnts():
    skinClusterName = cmds.ls (cmds.listHistory (cmds.ls (sl=True) ), type='skinCluster')[0]
    jointName = cmds.ls (cmds.listHistory (skinClusterName, levels=1), type='transform')
    cmds.select(jointName)
    return jointName

    