import maya.cmds as cmds
 
WIDTH =420
SFX = 'replaceReferens'

def replaceReferens(): 
    win = SFX+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t='', width=WIDTH,  height=10, s=False, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout (SFX+"ColumnL", adjustableColumn=True)
    cmds.frameLayout (  label="Replace referens"   , cll=0, w=WIDTH , bgc=[0,0,0], borderVisible=True)
    cmds.textFieldButtonGrp(SFX+"pathA", label='New file :  ', buttonLabel='   Add path  ', columnWidth3=[WIDTH*0.2, WIDTH*0.55, WIDTH*0.6], bc='addPath("'+SFX+'pathA")')
    cmds.textFieldButtonGrp(SFX+"pathB", label='Old file :  ', buttonLabel='   Add path  ', columnWidth3=[WIDTH*0.2, WIDTH*0.55, WIDTH*0.6], bc='addPath("'+SFX+'pathB")' )
    cmds.button(  l="Swap", c="swap()"  )
    cmds.showWindow (win)
    cmds.window (win, e=True,  height=120 )
    
def addPath(TFBG):
    dir_Name = cmds.fileDialog2( fileMode=1, caption="Add new path" )[0].split('/')[-1]
    cmds.textFieldButtonGrp(TFBG, e=True, text=dir_Name)
    
def swap():
    dir_Name = cmds.fileDialog2( fileMode=1, caption="Add new path" )[0]
    srs = cmds.textFieldButtonGrp(SFX+"pathA", q=True, text=True)
    trg = cmds.textFieldButtonGrp(SFX+"pathB", q=True, text=True)
    
    f = open(dir_Name)
    data=[]
    for line in f: 
        if trg in line:  
            line = line.replace( trg, srs)
            print trg, '  replaced by', srs
        data.append(line)      
    f.close()
    
    f = open(dir_Name, 'w')
    for line in data:  f.write(line)
    f.close()

 









