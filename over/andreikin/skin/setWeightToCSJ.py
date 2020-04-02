import maya.cmds as cmds
from anProcedures import *
from CharacterNames import CharacterNames as chn
import maya.mel as mm
from an_classSkin import AnSkinSys


def setWeightToCSJUI(): #sel order: jnt, elbow, elbow, wrist
    win = "SkinW"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="addCSJntWeight v1.0", width=320,  height=50, s=True, rtf=True, menuBar=True )
    cmds.columnLayout()
    #bc = "cmds.textFieldButtonGrp ('TFBG_G', e=True, tx=  cmds.ls (sl=True)[0]);"
    #cmds.textFieldButtonGrp('TFBG_G',  label='Geometry :    ',   buttonLabel='   add selection   ', bc=bc, columnWidth3=[150, 100, 100] )
    bc = "cmds.textFieldButtonGrp ('TFBG_J', e=True, tx=  cmds.ls (sl=True)[0]);"
    cmds.textFieldButtonGrp('TFBG_J',  label='   Jnt :    ',   buttonLabel='   add selection   ', bc=bc, columnWidth3=[150, 100, 100] )
    bc = "cmds.textFieldButtonGrp ('TFBG_CSJ', e=True, tx=  cmds.ls (sl=True)[0]);"
    cmds.textFieldButtonGrp('TFBG_CSJ',  label='CS Jnt :    ',   buttonLabel='   add selection   ', bc=bc, columnWidth3=[150, 100, 100] )
    cmds.floatSliderGrp('jntMaxWeight', label='Max weight :    ', field=True, minValue=0, maxValue=0.5,  value=0.1, step=0.01, columnWidth3=[150, 100, 100]  )

    cmds.rowColumnLayout (nc=2, cw=[(1, 252), (2, 100) ], columnSpacing=[(2,2),(3,2)], rowSpacing=[(2,2),(3,2) ])
    cmds.text("")
    cmds.button   (l='add weight',   c="setWeightToCSJ()" )
    cmds.showWindow( win )


def setWeightToCSJ ():
    #geo = cmds.textFieldButtonGrp ('TFBG_G', q=True, tx=True)
    jnt = cmds.textFieldButtonGrp ('TFBG_J', q=True, tx=True)
    csJnt = cmds.textFieldButtonGrp ('TFBG_CSJ', q=True, tx=True)
    jntMaxWeight = cmds.floatSliderGrp('jntMaxWeight', q=True, v=True)
    #cmds.selectPref (trackSelectionOrder=True)
    point =   cmds.ls( fl=True, orderedSelection=True)
    point.append(point.pop(2))# moove last point to index 3
    
    tmpPlane = cmds.polyPlane  ( n=chn(csJnt).divideName()[0]+chn(csJnt).divideName()[1]+'_plane',  sx=1,  sy=1) [0]
    for i in range(4):
        pos = cmds.xform( point[i], q=True, ws=True, t=True )
        cmds.xform( tmpPlane + '.vtx['+ str(i)+']' ,  ws=True, t=pos )
    mm.eval('polySplit -ch 1 -sma 180 -ep 0 0.03 -ep 3 0.03 |'+tmpPlane+';' )
    cmds.delete(tmpPlane, constructionHistory=True)
    skinClusterName = cmds.skinCluster(jnt, csJnt, tmpPlane, tsb=True, normalizeWeights=True)[0]  #skinning
    
    for i in range(6):
        if not i==4 :
            cmds.setAttr (skinClusterName + " .weightList["+str(i)+"].w[0]", 1.0 )
            cmds.setAttr (skinClusterName + " .weightList["+str(i)+"].w[1]", 0.0 )
        else :
            cmds.setAttr (skinClusterName + " .weightList["+str(i)+"].w[0]", 1.0-jntMaxWeight )
            cmds.setAttr (skinClusterName + " .weightList["+str(i)+"].w[1]", jntMaxWeight )
    
    geo =  point[0].split('.')[0]
    dupGeo = cmds.duplicate (geo, n='tmpCopy')[0]
        
    AnSkinSys('').copySkin( tmpPlane, dupGeo  )
    weightList = AnSkinSys(dupGeo). getSkinWeights()
    
    geoSkin = AnSkinSys(geo)
    geoSkin.getSkinWeights()
    geoSkin.insertJointsToWeightList (dupGeo, jnt)   
    geoSkin.setSkinWeights() 
    
    for each in [tmpPlane, dupGeo]:
        clusterName = cmds.ls (cmds.listHistory (each), type='skinCluster' )[0]
        cmds.skinCluster ( clusterName,  e=True, ub=True)
        cmds.delete(each)

























