
import maya.cmds as cmds
from  anProcedures import  * 
 
def an_deformSelector():
    geo  = cmds.ls(sl=True)[0]
    history = cmds.listHistory (geo)
    inputList=[]
    deformList = 'ffd', 'blendShape', 'skinCluster', 'wrap' , 'melnitsaWrap'
    for each in history:
        #print cmds.nodeType( each ) 
        if cmds.nodeType( each  ) in deformList:
            inputList.append(each)
    uiList = an_turnBasedUi('defList', title ='Deformers selector v.1',  stepsLabel =['', ])

    cmds.separator(st="none", h=3, p= uiList[0])
    for deform in inputList: 
        cmds.rowColumnLayout( numberOfColumns=4, columnWidth=[(1, 300), (2, 90), (3, 3), (4, 90)],    p= uiList[0], columnSpacing=[5, 5] )
        cmds.text('       '+deform+' ('+ cmds.nodeType( deform  )+')'   , align="left")
        cmds.button(l="Select influens", c='cmds.select(getDeformerInfluens("'+deform+'"))')
        cmds.text('')
        cmds.button(l="Delete deformer", c='cmds.delete("'+deform+'")')
 
    cmds.separator(st="none", h=3, p= uiList[0]) 
    cmds.button(l="Refresh", p= uiList[0], c='deformSelector()') 
        

def getDeformerInfluens(deformerNod):
    if cmds.nodeType(deformerNod) == 'ffd':
        influensShape=cmds.connectionInfo(deformerNod+'.deformedLatticeMatrix', sourceFromDestination =True).split('.')[0]
        return cmds.listRelatives(influensShape, p=True)[0]
    elif cmds.nodeType(deformerNod) == 'blendShape':  
        return cmds.blendShape( deformerNod, q=True, t=True )
    elif cmds.nodeType(deformerNod) == 'wrap': 
        influens=cmds.connectionInfo(deformerNod+'.smoothness[0]', sourceFromDestination =True).split('.')[0]
        return influens    
    elif cmds.nodeType(deformerNod) == 'skinCluster': 
        jointName = cmds.ls (cmds.listHistory (deformerNod, levels=1), type='transform')
    elif cmds.nodeType(deformerNod) == 'melnitsaWrap': 
        influensShape=cmds.connectionInfo(deformerNod+'.obstacleMesh', sourceFromDestination =True).split('.')[0]
        return cmds.listRelatives(influensShape, p=True)[0]             
