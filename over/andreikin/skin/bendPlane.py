



# 01.03.2019 add names and pfx

from an_classNames import AnNames
from  anProcedures import  *
import maya.cmds as cmds
from an_classSkin import AnSkinSys

def bendPlaneUi():
    vWin = "an_bendPlane"
    vWinHight =130
    vWinWeight=490
    if cmds.window (vWin, exists=True): cmds.deleteUI ( vWin, window=True )
    cmds.window  (vWin, t="Transfer skin  v 1.00", sizeable=False, wh= [vWinWeight, vWinHight], menuBar=True )
    cmds.columnLayout('cLayout' )
    cmds.separator   (h=2 )
    cmds.frameLayout('addLayout', label='Joint :',  lv=True, backgroundColor=[ 0, 0, 0 ], w= vWinWeight, marginWidth = 2)
    
    cmds.textFieldButtonGrp ('TFBG_object', l="Name:",  bl="<<Add selected",
        cw = [(1, 124), (2, 250)],  bc = "cmds.textFieldButtonGrp ('TFBG_object', e=True, tx=  AnNames(cmds.ls (sl=True)[0]).sfxMinus())" )
        
    cmds.intSliderGrp('ISGrp', label='Jnt num for prof:', cw = [(1, 124), (2, 20)], field=True, min=0, max=10,  v=0 ,  enable= True  )
    
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 140), (2, 140), (3, 140) ]  ) 
    for txt  in ['JCS joint A', 'JCS joint B', 'Skin joint']: cmds.text(txt)
    cmds.setParent( '..')
    cmds.rowColumnLayout( numberOfColumns=3, columnSpacing= ([1, 1], [2,1], [3,1]), p='cLayout' )
    cmds.button( label='Add joints', command= "an_uiBlock()", backgroundColor=[ 0.4, 0.4, 0.4 ], w= 163,)

    cmds.button( label='Refresh', command= 'refreshUi()', backgroundColor=[ 0.4, 0.4, 0.4 ], w= 163,)
    cmds.button( label='Create plane', command= "createPlane()", backgroundColor=[ 0.4, 0.4, 0.4 ], w= 163,)
    cmds.showWindow( vWin )
    cmds.window (vWin,e=True, height=vWinHight, w=vWinWeight )

def refreshUi():
    for x in cmds.frameLayout('addLayout', q=True, ca=True )[1:]: 
        cmds.deleteUI(x)
        cmds.window ("an_bendPlane",e=True, height=cmds.window ("an_bendPlane",q=True, height=True )-31 )
         
def an_uiBlock(): # ui which  is inserted to global ui for the each target
    vWin = "an_bendPlane"
    if cmds.ls(sl=True)[0]:
        cmds.window (vWin,e=True, height=cmds.window (vWin,q=True, height=True )+31 )
        layoutR = cmds.rowColumnLayout( numberOfColumns=8, columnWidth=[(1, 100), (2, 40), (3, 100), (4, 40), (5, 100), (6, 40),(7, 50)],  columnSpacing=[7, 1],  p='addLayout' )  
        for x in cmds.ls(sl=True):
            textFild = cmds.textField(tx=x  )
            bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
            cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc )
    
        if len(cmds.ls(sl=True))==1:
            for i in [0,1,2,3]:cmds.text(label='')
            
        bc1 = 'cmds.window ("'+vWin+'",e=True, height=cmds.window ("'+vWin+'",q=True, height=True )-31 );'
        bc2 = 'cmds.deleteUI("'+layoutR+'")'
        cmds.button(l='delete',  backgroundColor=[ 0.8, 0.4, 0.4 ], c = bc1+bc2)
        cmds.setParent( '..')

def createPlane( ):
    csJntWeight = 0.05
    pflJntId = cmds.intSliderGrp('ISGrp', q=True, v=True)# number of the join that will give the base profile
    
    jntList = []
    for eachLayout in cmds.frameLayout('addLayout', q=True, ca=True )[3:]:    #get joint list
        txtLayouts = cmds.rowColumnLayout(eachLayout, q=True, ca=True )
        jnts = [ cmds.textField(x, q=True, tx=True ) for x in txtLayouts if 'textField' in x]
        jntList.append(jnts)
    
    
    
    pos = [cmds.xform( x,  q=True,  t=True, ws=True ) for x in  jntList[pflJntId][:2]]
    ofsVal = [(pos[0][x]- pos[1][x])/2 for x in   [0,1,2]]
    
    pfx =cmds.textFieldButtonGrp ('TFBG_object', q=True, tx=True)
    
    planeTmp = cmds.polyPlane( n=pfx ,  sx=1, sy=len(jntList)-1)[0]
    
    pointWeightList={} # set 0 val for all points
    skinJnts = reduce(lambda a,b: a+b, jntList)
    for x in skinJnts: pointWeightList[x] =  [0 for i in  range( len(jntList)*2)]
    
    i=0 
    for jnts in jntList:
        if  len(jnts)==1 : # esli net correcttiv kostey   
                posTmp = cmds.xform( jnts,  q=True,  t=True, ws=True )
                pos = [ posTmp[x] + ofsVal[x] for x in   [0,1,2]]
                cmds.xform( planeTmp + '.vtx['+ str(i)+']' ,  ws=True, t=pos )
                pointWeightList[jnts[0]][i]=1  # set weight val
                
                i=i+1
                pos = [ posTmp[x] - ofsVal[x] for x in   [0,1,2]]
                cmds.xform( planeTmp + '.vtx['+ str(i)+']' ,  ws=True, t=pos )
                pointWeightList[jnts[0]][i]=1  # set weight val
                i=i+1   
        else: 
             for id in [0, 1]:  # esli  correcttiv kosti est`
                    pos = cmds.xform( jnts[id] ,  q=True,  t=True, ws=True )   
                    cmds.xform( planeTmp + '.vtx['+ str(i)+']' ,  ws=True, t=pos )
                    
                    pointWeightList[jnts[id]][i]=csJntWeight
                    pointWeightList[jnts[2]][i]=1.0-csJntWeight
                    print jnts [id], '___', jnts
                    i=i+1 
                                 
    self = AnSkinSys(planeTmp)
    self.weightList=pointWeightList
    self.setSkinWeights()




 