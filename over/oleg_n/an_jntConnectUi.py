 
import maya.cmds as cmds

sfx = 'jcu'

def an_jntConnectUi( ):
    win = sfx+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t=sfx + '_', width=420,  s=True, rtf=True, menuBar=True )
    
    ################################

    cmds.frameLayout ( 'fr1',  label="Matching: "  , cll=0, width=420,  bgc=[0,0,0], borderVisible=True, bgs=True)
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210)],  columnSpacing=[2, 2], rowSpacing=[2, 2]    ) 
    cmds.button( label='Match translation', c='an_match (  position=1)')
    cmds.button( label='Match rotation', c='an_match (  rotation=1)') 
    cmds.button( label='Match scaling', c= 'an_match (  scale=1)')
    cmds.button( label='Match pivot', c= 'an_match (  pivots=1)')
    cmds.button( label='Match all transforms', c= 'an_match ( pivots=1, position=1, rotation=1, scale=1)')
    #cmds.setParent( '..' )
    for _ in 1,2:     cmds.setParent( '..' )
   
    #################################
    
    cmds.frameLayout (sfx+"BaseL",  label="Connections :"  , cll=0, w=420, bgc=[0,0,0], borderVisible=True)
   
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210)],  columnSpacing=[2, 2], rowSpacing=[2, 2]    )  
 
    cmds.button( label='load to left', c='addObj( side = "CLeft")')
    cmds.button( label='load to right', c='addObj( side = "CRight")') 
    cmds.button( label='select left', c= 'cmds.select(getList("CLeft"))')
    cmds.button( label='select right', c= 'cmds.select(getList("CRight"))')

    cmds.radioButtonGrp(sfx+"RBG", label='      ', labelArray2=['parent', 'parentConstraint'], numberOfRadioButtons=2, p=sfx+"BaseL", sl=1 ) 
     
    cmds.setParent( '..' )
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210)],  columnSpacing=[2, 2], rowSpacing=[2, 2]    )  
    cmds.button( label='clear ui' ,     c = 'clearUi()') 
    cmds.button( label='connect left to right' ,     c = 'connect()' ) 
    for _ in 1,2,3:     cmds.setParent( '..' )
      
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210), ],   p=sfx+"BaseL", columnSpacing=[2, 10]   ) 
    cmds.columnLayout (sfx+"CLeft", width=200)
    cmds.setParent( '..' )
    cmds.columnLayout (sfx+"CRight", width=200 )  
    cmds.showWindow (win)

def clearUi():
    for side in ['CLeft','CRight' ]:
        for each in [x for x in  cmds.columnLayout (sfx+side, q=True, ca=True)]:
            cmds.deleteUI(each)

def an_match ( pivots=False, position=False, rotation=False, scale=False):
    seursLst = getList('CLeft')
    targLst = getList('CRight')
    ln = min(len(seursLst), len(targLst))
    for i in range(ln):
         cmds.matchTransform(seursLst[i], targLst[i], pivots=pivots, position=position, rotation=rotation, scale=scale)

def connect():
    seursLst = getList('CLeft')
    targLst = getList('CRight')
    ln = min(len(seursLst), len(targLst))
    for i in range(ln):
        if cmds.radioButtonGrp(sfx+"RBG", q=True, sl=True ) == 1:  #parent
             cmds.parent(seursLst[i], targLst[i])
             
        if cmds.radioButtonGrp(sfx+"RBG", q=True, sl=True ) == 2:  #parentConstraint
             cmds.parentConstraint(targLst[i], seursLst[i], mo=True)

def objUi(obj, prt):
    cmds.rowColumnLayout(obj+'ui', nc=4 , columnWidth=[(1, 80), (2, 35), (3, 50), (4, 35)],  p=prt, columnSpacing=([3, 1],[4, 1])    ) 
    cmds.text(obj+'T', label = obj)
    
    com = 'cmds.text("'+obj+'T", e=True,  label = cmds.ls(sl=1)[0] )' 
    
    cmds.button(label='Sel', width=34, c='cmds.select("'+obj+'")')
    cmds.button(label='Reload', width=49, c=com)
    cmds.button(label='Del', width=34, c='cmds.deleteUI("'+obj+'ui")', al='center')


def getList(side): #"CLeft"
    if cmds.columnLayout (sfx+side, q=True, ca=True):
        #return [x[:-2] for x in  cmds.columnLayout (sfx+side, q=True, ca=True)]
        return [ cmds.text(x[:-2]+'T', q=1,  label = 1) for x in  cmds.columnLayout (sfx+side, q=True, ca=True)]
    else: 
        return False

def addObj( side = "CLeft"):
    objs= cmds.ls(sl=1)
    for obj in objs:
        if not getList(side) or  not obj in  getList(side) :
            objUi(obj, sfx+side)


 
#an_jntConnectUi()

 



 