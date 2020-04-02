import maya.cmds as cmds 

def an_selectVertexByColor():
    geo=cmds.ls(sl=1)[0]
    pointNum = cmds.getAttr (geo + ".cp", size=True )  
    
    colorList=[]
    for i in xrange(pointNum):
        pColor = cmds.polyColorPerVertex(geo+'.vtx['+str(i)+']',  query=True, r=True, g=True, b=True )
        rColor = [round(x , 6) for x in pColor]
        if not rColor in colorList: colorList.append(rColor)
    
    v_win = "colorWin1"
    if cmds.window (v_win, exists=True):
        cmds.deleteUI (v_win)
    cmds.window(v_win, t="Ik/fk rope rig tools v.1", w=80, h=100)
    cmds.columnLayout(adj=1)
    for pColor in colorList:
        cmds.button (bgc =  pColor, l=" ", c= 'selectPoints("'+geo+'", ['+str(pColor[0])+', '+ str(pColor[1])+', '+str(pColor[2])+ '])' )
    
    cmds.button ( l='Refresh', c='an_selectVertexByColor()'  )
    
    cmds.showWindow(v_win)
 



def selectPoints(geo, pColor):
    print pColor
    
    
    pointNum = cmds.getAttr (geo + ".cp", size=True )
    selPoints = []
    for i in xrange(pointNum):
        curentColor = cmds.polyColorPerVertex(geo+'.vtx['+str(i)+']',  query=True, r=True, g=True, b=True )
        if [round(x , 6) for x in curentColor] == pColor: selPoints.append(geo+'.vtx['+str(i)+']')
    cmds.select(selPoints)


 

