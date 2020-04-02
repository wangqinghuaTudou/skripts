import maya.cmds as mc
import maya.api.OpenMaya as om
import time  as time

def guTransferAttrs():
	copyMethList = ['components', \
	                'topology', \
	                'world', \
	                'local', \
	                'UV']
	win = 'guTransferMaping'
	if mc.window(win, exists=True):
	    mc.deleteUI(win)
	win = mc.window(win, title='transfer attributes', \
	                width=300, \
	                height=200, \
	                sizeable=False)
	mc.columnLayout ('guMainLayoutTransferMaping', \
	                 width=300, \
	                 height=200, \
	                 adjustableColumn=True)
	mc.rowColumnLayout('guRowLayoutCopyMeth', numberOfColumns=2, \
	                   columnAttach=[1, 'right', 10], \
	                   columnWidth=[[1, 120], [2, 170]])
	mc.text('guTextCopyMethList', label='Copying Method:', align='right')
	mc.optionMenuGrp('guOptMenuGrpCopyMethList', columnWidth=[1, 80])
	for item in copyMethList:
		mc.menuItem(label=item)

	mc.setParent('..') 
	mc.checkBox( 'guVertexPosition',label='vertex position', align='left')
	mc.checkBox( 'guVertexNormal',label='vertex normal', align='left')
	mc.checkBox( 'guUvSets',label='Uv Sets', align='left')
	mc.checkBox( 'guColorSets',label='Color Sets', align='left')
	mc.separator(height=5, style='in')
	mc.setParent('..') 
	mc.columnLayout (width=100, \
	                 height=110, \
	                 adjustableColumn=True)	                 
	mc.checkBox( 'guCleanOrig',label='clean Orig Shapes', align='left',v=True)
	mc.button( label='Transfer Attrs', align='center', command='guTransfer()' )
	      
	mc.showWindow(win)
	


def guSelectObjcts():
    sel=mc.ls(sl=True)
    if len(sel)<2:
        mc.error('for tranffer pease select more then one object')
    return sel

def guOrigShape(sel):
    orig=[x for x in mc.listRelatives(sel[1],c=True,s=True) if mc.getAttr(x+'.intermediateObject') == 1]
    if orig:
        if mc.checkBox( 'guCleanOrig',q=True,v=True):
            oldOrig=orig
            for i in oldOrig:
                if not mc.listConnections(i+'.worldMesh[0]'):
                    mc.delete(i)
                    om.MGlobal.displayInfo(i+'     --- was deleted')
                else:
                    orig=i
    
    return mc.listRelatives(sel[1],c=True,s=True)
    
def guSwichOrigAndShape(shapes):
    if len(shapes)>1:
        for i in shapes:
            if mc.getAttr(i+'.intermediateObject')==1:
                mc.setAttr(i+'.intermediateObject',0)
            else:
                mc.setAttr(i+'.intermediateObject',1)
    
            

def guGetPorametrs():
    NormalCopyMethList = ['', \
                    	  'world', \
                          'local', \
                          'UV',
                          'components', \
                          'topology']
    smplSpac= NormalCopyMethList.index(mc.optionMenuGrp('guOptMenuGrpCopyMethList',q=True,v=True))    
    transferPositions= mc.checkBox( 'guVertexPosition',q=True,v=True)
    transferNormals= mc.checkBox( 'guVertexNormal',q=True,v=True)
    transferUVs= mc.checkBox( 'guUvSets',q=True,v=True)
    transferColors= mc.checkBox( 'guColorSets',q=True,v=True)
    return transferPositions,transferNormals,transferUVs,transferColors,smplSpac

def guTransferAttr(sel,shapes,(transferPositions,transferNormals,transferUVs,transferColors,smplSpac)):
    if transferColors:
        colorSet=mc.polyColorSet(sel[1:],cs=True,q=True)
        if colorSet:
            mc.polyColorSet(delete=True,colorSet=colorSet)
    result=mc.transferAttributes (sel, \
                           transferPositions= transferPositions, \
                           transferNormals= transferNormals, \
                           transferUVs= transferUVs*2, \
                           transferColors= transferColors*2, \
                           sampleSpace= smplSpac, \
                           sourceUvSpace="map1", \
                           targetUvSpace="map1", \
                           searchMethod=3, \
                           flipUVs=0, \
                           colorBorders=1)
    if len(shapes)>1:
            mc.delete(sel[1:],ch=True)
    om.MGlobal.displayInfo('transfer method  ---- ('+str(smplSpac)+') its: '+mc.optionMenuGrp('guOptMenuGrpCopyMethList',q=True,v=True))
    om.MGlobal.displayInfo('transfer vertex position ---  '+str(transferPositions*1))
    om.MGlobal.displayInfo('transfer vertex normal ---    '+str(transferNormals*1))
    om.MGlobal.displayInfo('transfer uv ---               '+str(transferUVs*2))
    om.MGlobal.displayInfo('transfer color sets ---       '+str(transferColors*2))
    om.MGlobal.displayInfo('delete history ---            '+str(sel[1:]))
    return result

def guTransfer():
    sel=guSelectObjcts()
    shapes=guOrigShape(sel)
    om.MGlobal.displayInfo('transfer from\\to '+str(sel))  
    if mc.checkBox( 'guColorSets',q=True,v=True):
        mc.delete(guTransferAttr(sel,[],guGetPorametrs()))
    guSwichOrigAndShape(shapes)
    guTransferAttr(sel,shapes,guGetPorametrs())
    guSwichOrigAndShape(shapes)


#guTransferAttrs()



