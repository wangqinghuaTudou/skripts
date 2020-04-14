import maya.cmds as cmds


SFX = 'jcu'
WIN_SIZE = [420, 250]
WIN_NAME = SFX+"Win"

def an_jntConnectUi( ):
    if  cmds.window (WIN_NAME, exists=True ): cmds.deleteUI (WIN_NAME)
    cmds.window (WIN_NAME, t='an_connector', wh=WIN_SIZE,  s=True, rtf=True, menuBar=True )

    cmds.frameLayout ( 'fr1',  label="Matching: "  , cll=0, h= 30, w=WIN_SIZE[0], bv=True, bgs=True,  bgc=[0,0,0],)
    cmds.rowColumnLayout( numberOfColumns=2 , cw=[(1, WIN_SIZE[0]/2), (2, WIN_SIZE[0]/2)],  cs=[2, 2], rs=[2, 2]   ) 
    cmds.button( label='Match translation', c='an_match (  position=1)')
    cmds.button( label='Match rotation', c='an_match (  rotation=1)') 
    cmds.button( label='Match scaling', c= 'an_match (  scale=1)')
    cmds.button( label='Match pivot', c= 'an_match (  pivots=1)')
    cmds.button( label='Match all transforms', c= 'an_match ( pivots=1, position=1, rotation=1, scale=1)')
    for _ in 1,2:     cmds.setParent( '..' )
    
    cmds.frameLayout (SFX+"BaseL",  label="Connections :"  , cll=0, w=WIN_SIZE[0], bgc=[0,0,0], borderVisible=True)
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, WIN_SIZE[0]/2), (2, WIN_SIZE[0]/2)],  columnSpacing=[2, 2], rowSpacing=[2, 2]    )  
 
    cmds.button( label='Load to left', c='addObj( side = "CLeft")')
    cmds.button( label='Load to right', c='addObj( side = "CRight")') 
    cmds.button( label='Select left', c= 'cmds.select(getList("CLeft"))')
    cmds.button( label='Select right', c= 'cmds.select(getList("CRight"))')
    cmds.button( label='Clear left' ,     c = 'clearUi("CLeft")') 
    cmds.button( label='Clear right' ,     c = 'clearUi("CRight")') 

    cmds.radioButtonGrp(SFX+"RBG", label='      ', labelArray2=['parent', 'parentConstraint'], numberOfRadioButtons=2, p=SFX+"BaseL", sl=1 ) 
    cmds.setParent( '..' )
    
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210)],  columnSpacing=[2, 2], rowSpacing=[2, 2]    )  
    cmds.button( label='Clear all' ,     c = 'clearUi("CLeft"); clearUi("CRight")') 
    cmds.button( label='Connect left to right' ,     c = 'connect()' ) 
    for _ in 1,2,3:     cmds.setParent( '..' )
      
    cmds.rowColumnLayout( numberOfColumns=2 , columnWidth=[(1, 215), (2, 210), ],   p=SFX+"BaseL", columnSpacing=[2, 10]   ) 
    cmds.columnLayout (SFX+"CLeft", width=200)
    cmds.setParent( '..' )
    cmds.columnLayout (SFX+"CRight", width=200 )  
    cmds.showWindow (WIN_NAME)
    updateSize()


def updateSize(): 
    child = [] 
    for side in ['CLeft','CRight' ]:
        if cmds.columnLayout (SFX+side, q=True, ca=True):
            ch_num = len(cmds.columnLayout (SFX+side, q=True, ca=True))
            child.append( ch_num)
    print child
    if child:
        cmds.window (WIN_NAME,  e=True, w=WIN_SIZE[0],  h=WIN_SIZE[1]+max(child)*25 )
    else :
        cmds.window (WIN_NAME,  e=True, wh=WIN_SIZE  )

def clearUi(side):
    if cmds.columnLayout (SFX+side, q=True, ca=True):
        for each in cmds.columnLayout (SFX+side, q=True, ca=True):
            cmds.deleteUI(each)
    updateSize()

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
        if cmds.radioButtonGrp(SFX+"RBG", q=True, sl=True ) == 1:  #parent
             cmds.parent(seursLst[i], targLst[i])
             
        if cmds.radioButtonGrp(SFX+"RBG", q=True, sl=True ) == 2:  #parentConstraint
             cmds.parentConstraint(targLst[i], seursLst[i], mo=True)

def objUi(obj, prt):
    cmds.rowColumnLayout(obj+'ui', nc=4 , columnWidth=[(1, 65), (2, 35), (3, 50), (4, 35)],  p=prt, columnSpacing=([3, 1],[4, 1])    ) 
    cmds.text(obj+'T', label = obj)
    
    com = 'cmds.text("'+obj+'T", e=True,  label = cmds.ls(sl=1)[0] )' 
    
    cmds.button(label='Sel', width=34, c='cmds.select("'+obj+'")')
    cmds.button(label='Reload', width=49, c=com)
    cmds.button(label='Del', width=34, c='cmds.deleteUI("'+obj+'ui"); updateSize()', al='center')


def getList(side): #"CLeft"
    if cmds.columnLayout (SFX+side, q=True, ca=True):
        #return [x[:-2] for x in  cmds.columnLayout (SFX+side, q=True, ca=True)]
        return [ cmds.text(x[:-2]+'T', q=1,  label = 1) for x in  cmds.columnLayout (SFX+side, q=True, ca=True)]
    else: 
        return False

def addObj( side = "CLeft"):
    objs= cmds.ls(sl=1)
    for obj in objs:
        if not getList(side) or  not obj in  getList(side) :
            objUi(obj, SFX+side)
    updateSize()



 



 