import maya.cmds as cmds

SFX = 'jcu'
WIN_SIZE = [420, 800]
WIN_NAME = SFX+"Win"
BUTT_SIZE = [WIN_SIZE[0]/2, 25]


def an_jntConnectUi( ):
    if  cmds.window (WIN_NAME, exists=True ): cmds.deleteUI (WIN_NAME)
    cmds.window (WIN_NAME, t='an_connector', wh=WIN_SIZE,  s=False, rtf=True  )
    cmds.columnLayout(  ) 
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(BUTT_SIZE[0], 25)  )
    
    cmds.text("Matching: ", h=25, fn = "boldLabelFont", bgc=[0,0,0]  );  cmds.text(" ",  bgc=[0,0,0]  )
    but('Match translation', 'an_match(position=1)')
    but('Match rotation', 'an_match(rotation=1)')
    but('Match scaling', 'an_match (  scale=1)')
    but('Match pivot', 'an_match (  pivots=1)')
    but('Match all transforms', 'an_match ( pivots=1, position=1, rotation=1, scale=1)')
    cmds.text(" ")
    cmds.text("Connections : ", h=25, fn = "boldLabelFont",  bgc=[0,0,0]);  cmds.text(" ",  bgc=[0,0,0])
    cmds.setParent( '..' )
    cmds.gridLayout( numberOfColumns=1, cellWidthHeight=(420, 25)   )
    cmds.radioButtonGrp(SFX+"RBG", label=' ', labelArray2=['parent', 'parentConstraint'], numberOfRadioButtons=2,  sl=1 )
    cmds.setParent( '..' )
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(BUTT_SIZE[0], 25))
    but('Load to left', 'addObj( side = "CLeft")')
    but('Load to right', 'addObj( side = "CRight")') 
    but('Select left', 'cmds.select(getList("CLeft"))')
    but('Select right',  'cmds.select(getList("CRight"))')
    but('Clear left' ,   'clearUi("CLeft")') 
    but('Clear right' ,  'clearUi("CRight")') 
    but('Clear all' ,  'clearUi("CLeft"); clearUi("CRight")') 
    but('Connect left to right' ,  'connect()') 
    cmds.setParent( '..' ) 
    cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(BUTT_SIZE[0], 540)  )
    cmds.scrollLayout (SFX+"CLeft", width=200)
    cmds.setParent( '..' )
    cmds.scrollLayout (SFX+"CRight", width=200) 
    cmds.showWindow (WIN_NAME)
    cmds.window (WIN_NAME,  e=True, w=WIN_SIZE[0],  h=WIN_SIZE[1])

def but(lbl, com):
    cmds.gridLayout( numberOfColumns=1, cellWidthHeight=(208, 23)  )
    cmds.button( label=lbl, c=com)
    cmds.setParent( '..' )

def clearUi(side):
    if cmds.scrollLayout (SFX+side, q=True, ca=True):
        for each in cmds.scrollLayout (SFX+side, q=True, ca=True):
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
        if cmds.radioButtonGrp(SFX+"RBG", q=True, sl=True ) == 1:  #parent
             cmds.parent(seursLst[i], targLst[i])
             
        if cmds.radioButtonGrp(SFX+"RBG", q=True, sl=True ) == 2:  #parentConstraint
             cmds.parentConstraint(targLst[i], seursLst[i], mo=True)

def objUi(obj, prt):
    cmds.rowColumnLayout(obj+'ui', nc=4 , columnWidth=[(1, 60), (2, 35), (3, 50), (4, 35)],  p=prt, columnSpacing=([3, 1],[4, 1])    ) 
    cmds.text(obj+'T', label = obj)
    
    com = 'cmds.text("'+obj+'T", e=True,  label = cmds.ls(sl=1)[0] )' 
    
    cmds.button(label='Sel', width=34, c='cmds.select("'+obj+'")')
    cmds.button(label='Reload', width=49, c=com)
    cmds.button(label='Del', width=34, c='cmds.deleteUI("'+obj+'ui")', al='center')


def getList(side): #"CLeft"
    if cmds.scrollLayout (SFX+side, q=True, ca=True):
        return [ cmds.text(x[:-2]+'T', q=1,  label = 1) for x in  cmds.scrollLayout (SFX+side, q=True, ca=True)]
    else: 
        return False

def addObj( side = "CLeft"):
    objs= cmds.ls(sl=1)
    for obj in objs:
        if not getList(side) or  not obj in  getList(side) :
            objUi(obj, SFX+side)
  



 



 