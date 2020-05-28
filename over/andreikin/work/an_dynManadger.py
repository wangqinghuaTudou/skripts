import maya.cmds as cmds
import maya.mel as mm
from an_Procedures.utilities import * 
from an_Procedures.dynamics import *

SFX = 'dMan'
WIN_SIZE = [600, 800]
WIN_NAME = SFX+"Win"
BUTT_SIZE = [WIN_SIZE[0]/2, 25]



 


def dynObg(name, addVis = False  ):
    
    cmds.checkBox( v=1, l='solv')
    if  addVis: cmds.checkBox( v=0, l='vis')
    else: cmds.text(" ")
    cmds.text("   "+name, al="left")
    cmds.button( l='Select', c='dynObgButtomComand("'+name+'")' ) 
    
    cmds.button( l='AE' , c='dynObgButtomComand("'+name+'", type = "AE" )' )
    cmds.button( l='Copy' ) 
    cmds.button( l='Past' )

def dynObgButtomComand (name, type = 'select' ):
    if type == 'select': 
        if  cmds.nodeType(name)=='nucleus' : cmds.select(name)
        elif  cmds.nodeType(name)=='nRigid' : pass
        
        #if cmds.nodeType(name)=='nucleus':pass
        
        
        #name = cmds.listRelatives(name, p=True)[0]
        
        #cmds.select(name)
        #print 'hjkgjk'
        
    elif type == 'AE': 
        cmds.select(name)
        mm.eval('AttributeEditor;') 
 
 
 
 
 
 
 
 
def heder(txt, bgc):
    for _ in range(2): cmds.canvas(bgc = bgc)
    cmds.text(txt, al="left", bgc= bgc)
    for _ in range(4): cmds.canvas(bgc = bgc)
 

def nucleusUi(nucleus):
    
    cmds.frameLayout(nucleus+"FL",  label=nucleus, bgc=[0,0,0] , cll=True)
    
    bSize=60
    size = [(1, 60),   (2,60),  (3, 220),  (4, bSize),   (5, bSize),   (6, bSize),  (7, bSize)]  
    
    cmds.rowColumnLayout( numberOfColumns=len(size), columnWidth=size,   )
    dynObg(nucleus, addVis = 1 )
 
    heder("  Cloth objects : ", [0.2]*3)
 
    cloths, colliders, constraints = getDataFromNucleas(nucleus)
 
    for cloth in  cloths:  dynObg(cloth )
        
    heder("   Colliders : ", [0.2]*3)
    
    for collider in  colliders:  dynObg(collider  )      
    
    
def an_dynManadgerUi():
    if  cmds.window (WIN_NAME, exists=True ): cmds.deleteUI (WIN_NAME)
    cmds.window (WIN_NAME, t='an_connector', wh=WIN_SIZE,  s=False, rtf=True  )
    cmds.columnLayout(  ) 

    cmds.scrollLayout (SFX+"mine", width=WIN_SIZE[0])
    nucleusUi("nucleus1")
    
    #for _ in range(50):
       # cmds.button(  ) 
 
    cmds.showWindow (WIN_NAME)
    cmds.window (WIN_NAME,  e=True, w=WIN_SIZE[0],  h=WIN_SIZE[1])


an_dynManadgerUi()

def but(lbl, com):
    cmds.gridLayout( numberOfColumns=1, cellWidthHeight=(208, 23)  )
    cmds.button( label=lbl, c=com)
    cmds.setParent( '..' )
 
 

def getDynamicsData():
    referenceList =  [x for x in  cmds.ls(rf = True) if not cmds.file(rfn=x, q=True, deferReference=True )]
    #file -unloadReference "BabushkaMiddleRN" "D:/work/Project/MALYSH/assets/chars/babushka/maya/babushka_dyn.mb"
    cmds.file(  query=True, referenceNode=True )
    cmds.file("BabushkaMiddleRN",   loadReference=True)