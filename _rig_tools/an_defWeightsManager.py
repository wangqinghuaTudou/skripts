import maya.cmds as cmds
from anProcedures import *

def an_defWeightsManager():
    win = "defWeightsManager"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Deformers weights manager v1.00", width=420,  height=420, s=False, rtf=True, menuBar=True )
    cmds.columnLayout (  adjustableColumn=True, rowSpacing=1)
    cmds.canvas(  height=5 )
    tabs = cmds.tabLayout('TL' )
    cmds.tabLayout( tabs, edit=True, tabLabel=( (copyWeightsTab(),  'Copy / Mirror'),
                                                (saveTab(), 'Save weights')))
    cmds.showWindow()
    #cmds.window (win, e=True,    height=220  )
    
def copyWeightsTab():
    child1 = cmds.columnLayout ("CopyCL", adjustableColumn=True, rowSpacing=5)
    cmds.canvas(  height=5 )
    cmds.radioButtonGrp('RBG', numberOfRadioButtons=3, label='Axis  :    ', labelArray3=['X', 'Y', 'Z'], sl=1, cw4= [159, 50, 50, 50] )
    for TFBG, lable in zip( ['TFBG1', 'TFBG2', 'TFBG3', 'TFBG4'], ['Source mesh', 'Source deformer', 'Destanation mesh',  'Destanation deformer']  ):
        my_tfbgTFBG(TFBG, lable)  
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 148), (2, 220)] ) 
    cmds.text('Surface association :', al='right')
    cmds.optionMenuGrp('OptMenGrp', columnWidth=[1, 60])
    for item in ["closestPoint", "rayCast", "closestComponent"]:
        cmds.menuItem(label=item)
    cmds.setParent( '..' )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 210), (2, 210)] )
    cmds.button(l='Mirror weights', c='an_mirrorWeights()')
    cmds.button(l='Copy weights', c='an_copyDefWeights()')
    for i in range(2): cmds.setParent( '..' )
    return child1
    
def saveTab():
    child1 = cmds.columnLayout ("SaveCL", adjustableColumn=True, rowSpacing=5)
    cmds.canvas(  height=5 )
    for TFBG, lable in zip( ['TFBG5', 'TFBG6' ], ['Mesh', 'Deformer']  ):
        my_tfbgTFBG(TFBG, lable)
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 210), (2, 210)] )
    cmds.button(l='Save weights', c='an_saveDeformerMask()')
    cmds.button(l='Load weights', c='an_loadDeformerMask()')
    for i in range(2): cmds.setParent( '..' )
    return child1


def my_tfbgTFBG(TFBG, lable):
    cmds.rowColumnLayout(TFBG, numberOfColumns=3, columnWidth=[(1, 150), (2, 160), (3, 110) ] )
    cmds.text(lable+' : ', al='right')
    cmds.textField(TFBG+'TF')
    cmds.button(l='Add selection',  c = 'cmds.textField("'+TFBG+'TF", e=True, tx = cmds.ls(sl=True)[0])')
    cmds.setParent( '..' )
    
#an_defWeightsManager()

def an_copyComand(srsMesh, srsDef, destMesh, destDef):
    cmds.copyDeformerWeights ( destinationDeformer = destDef, 
                              destinationShape = cmds.listRelatives(destMesh, s=True)[0], 
                              noMirror= True, 
                              sourceDeformer = srsDef, 
                              surfaceAssociation = cmds.optionMenuGrp('OptMenGrp', q=True, value=True),
                              sourceShape = cmds.listRelatives(srsMesh, s=True)[0] )

def an_copyDefWeights():
    srsMesh, srsDef, destMesh, destDef = [cmds.textField('TFBG'+str(i)+'TF', q=True, tx=True) for i in range(1, 5)]
    if srsMesh == destMesh:
        weight = an_getDeformerMask(srsMesh, srsDef)
        an_setDeformerMask(srsMesh, destDef, weight)
    else:
        an_copyComand(srsMesh, srsDef, destMesh, destDef)


def an_mirrorWeights():
    
    axis = ['X', 'Y', 'Z'][cmds.radioButtonGrp('RBG',  q=True, sl=True )-1]
    srsMesh, srsDef, destMesh, destDef = [cmds.textField('TFBG'+str(i)+'TF', q=True, tx=True) for i in range(1, 5)]
    tmp = cmds.duplicate(srsMesh)[0]
    clast=cmds.cluster ( tmp )[0] 
    weight = an_getDeformerMask(srsMesh, srsDef)
  
    an_setDeformerMask(tmp, clast, weight)
    cmds.setAttr ( tmp + ".scale"+axis,  cmds.getAttr ( tmp + ".scale"+axis)*-1)
    an_copyComand(tmp, clast, destMesh, destDef)
    cmds.delete(tmp, clast)




def an_getDeformerMask(Mesh, deformerNode): #get weights
    VertexNb = cmds.polyEvaluate(Mesh, v=1) 
    weight = cmds.getAttr('{0}.weightList[0].weights[0:{1}]'.format(deformerNode, VertexNb - 1))
    #st = cmds.connectionInfo( deformerNode+'.message', destinationFromSource=True)[0].split('.')[0]
    #pList =  an_convertPointsNames( cmds.sets( st, q=True ))
    #setVertList =[ int(x.split('[')[1].split(']')[0]) for x in  pList ]
    #for i in range(VertexNb): 
        #if not i in setVertList: weight[i] = 0.0
    return weight

def an_setDeformerMask(Mesh, deformerNode, weight): #set weights
    VertexNb = cmds.polyEvaluate(Mesh, v=1)
    tmpWeight = [0.0]*VertexNb
    cmds.setAttr('{0}.weightList[0].weights[0:{1}]'.format(deformerNode, VertexNb - 1), *tmpWeight, size=len(weight)) 
    cmds.setAttr('{0}.weightList[0].weights[0:{1}]'.format(deformerNode, VertexNb - 1), *weight, size=len(weight)) 

def an_saveDeformerMask():
    Mesh, deformerNode = [cmds.textField('TFBG'+str(i)+'TF', q=True, tx=True) for i in range(5, 7)]
    weight = an_getDeformerMask(Mesh, deformerNode)
    an_saveLoadData(data=weight, obgect='', delAttr = False, vDir='')

def an_loadDeformerMask():
    Mesh, deformerNode = [cmds.textField('TFBG'+str(i)+'TF', q=True, tx=True) for i in range(5, 7)]
    weight = an_saveLoadData( delAttr = False, vDir='')
    an_setDeformerMask(Mesh, deformerNode, weight)





































 
