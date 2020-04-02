import maya.mel as mm
import maya.cmds as cmds
import cPickle
vWidth=119

def an_bshMask():
    vWin = "an_setMaker"
    if  cmds.window (vWin, exists=True ): cmds.deleteUI (vWin)
    cmds.window (vWin, t="BlendShape mask tool.v02",  menuBar=True )
    cmds.menu (label="Edit" )
    cmds.menu (label="Help" )
    CLayout =cmds.columnLayout()
    cmds.frameLayout( label="Select vertices in particular order and save it in object's attribute:",  borderStyle='etchedIn' , cll=True, mw=2, mh=2)
    cmds.separator( style='none', h=1)
    cmds.textFieldGrp("markFBG", label="Input mark :", cw2=[180, 170 ] )
    cmds.intSliderGrp('rowISG1', field=True, label='Number of vertices rows :', cw3=[180, 80, 130], min=0, max=20, fieldMinValue=0, fieldMaxValue=100, value=4 )
    cmds.columnLayout("vButtonLayout").split('|')[-1]
    cmds.radioButtonGrp('verRBG1', numberOfRadioButtons=2, label='If you click button :      ', labelArray2=['Add selected', 'Select vertex'], sl = 1, cw3= [200,100,100] )
    cmds.separator( style='in' )
    an_vertexColumnUI("vButtonLayout")
    cmds.setParent( '..' )
    cmds.rowColumnLayout ( numberOfColumns=8, columnWidth=[(1, 12), (2, vWidth), (3, 5), (4, vWidth), (5, 5), (6, vWidth), (7, 5), (8, vWidth)])
    cmds.text (l="")
    cmds.button (label='Create rows', c="an_vertexColumnUI('vButtonLayout')")
    cmds.text (l="")
    cmds.button (label='Select set', c="an_selSet()")
    cmds.text (l="")
    cmds.button (label='Load set', c="an_selectSetFromObj()" )
    cmds.text (l="")
    cmds.button (label='Save selected set', c="an_recordToObg( )" )
    for i in [0,1]: cmds.setParent( '..' )
    an_1RampUi()
    cmds.showWindow ()

def an_1RampUi():
    cmds.frameLayout( label='Divide weight on two parts:', borderStyle='etchedIn', cll=True, w=510)
    cmds.separator( style='none' )
    cmds.textFieldButtonGrp ("bshTFBG", label="Channel in blendShape :", cw3=[180, 180, 50],  bl="   add  selected  ", bc= "an_filTextfild()")
    cmds.separator( style='in' )
    cmds.rowColumnLayout ( numberOfColumns=5, columnWidth=[(1, 180), (2, 50), (3, 50), (4, 50), (5, 50)])
    cmds.text (l="Interpolation :  ", align="right" )
    cmds.button (label='none' , c ="cmds.gradientControlNoAttr( 'falloffCurve', e=True, civ=0)" )
    cmds.button (label='Linear', c ="cmds.gradientControlNoAttr( 'falloffCurve', e=True, civ=1)"  )
    cmds.button (label='Smooth', c ="cmds.gradientControlNoAttr( 'falloffCurve', e=True, civ=2)"  )
    cmds.button (label='Spline', c ="cmds.gradientControlNoAttr( 'falloffCurve', e=True, civ=3)"  )
    cmds.setParent( '..' )
    cmds.rowColumnLayout ( numberOfColumns=4, columnWidth=[(1, 173), (2, 214), (3, 20), (4, 214)])
    cmds.text (l="")
    cmds.optionVar(stringValueAppend=['falloffCurveOptionVar', '0,1,2'])
    cmds.optionVar(stringValueAppend=['falloffCurveOptionVar', '1,0,2'])
    cmds.gradientControlNoAttr( 'falloffCurve', h=90)
    cmds.gradientControlNoAttr( 'falloffCurve', e=True, optionVar='falloffCurveOptionVar' )
    cmds.setParent( '..' )
    cmds.rowColumnLayout ( numberOfColumns=6, columnWidth=[(1, 137), (2, vWidth), (3, 5), (4, vWidth), (5, 5), (6, vWidth)])
    cmds.text (l="")
    cmds.button (label='Set gradient', c="an_makeGradient('direct')"  )
    cmds.text (l="")
    cmds.button (label='Residual part', c="an_makeGradient('mid')" )
    cmds.text (l="")
    cmds.button (label='Invert gradient', c="an_makeGradient('invert')"  )
    for i in [0,1]: cmds.setParent( '..' )


def an_makeGradient( vType):
    vVert = an_getValUI( )
    vBshFild = cmds.textFieldButtonGrp ("bshTFBG", q=True,  text=True )
    vBsh = vBshFild.split('.')[0]
    vTmp = cmds.aliasAttr( vBsh, query=True )

    for vI, vEach   in  enumerate(vTmp):
        if vEach == vBshFild.split('.')[1]:
            vBshId= int(vTmp[vI+1].split('[')[1].split(']')[0])
    for vPart in vVert:
        if vType == "direct": anSetGradient(vPart[::1], vBsh, vBshId )
        if vType == "invert": anSetGradient(vPart[::-1], vBsh, vBshId )
        if vType == "mid": anSetResidualGradient(vPart[::-1], vBsh, vBshId )

def anSetResidualGradient(vVertex, vBsh, vBshId):
    for vI, vEach   in  enumerate(vVertex):
        if  vEach:
            vpId=  vEach.split('tx[')[1].split(']')[0]
            vPos= 1.0/(len(vVertex)-1)*vI
            vVal = cmds.gradientControlNoAttr( 'falloffCurve', q=True, valueAtPoint=vPos )
            vInvVal = cmds.gradientControlNoAttr( 'falloffCurve', q=True, valueAtPoint=(1-vPos) )

            vVal =1-(vVal+vInvVal) if (vInvVal+vVal<1) else 0
            cmds.setAttr (vBsh+'.inputTarget[0].inputTargetGroup['+str(vBshId)+'].targetWeights['+str(vpId)+']', vVal)


def anSetGradient(vVertex, vBsh, vBshId):
    for vI, vEach   in  enumerate(vVertex):
        if  vEach:
            vpId=  vEach.split('tx[')[1].split(']')[0]
            vPos= 1.0/(len(vVertex)-1)*vI
            vVal = cmds.gradientControlNoAttr( 'falloffCurve', q=True, valueAtPoint=vPos )
            cmds.setAttr (vBsh+'.inputTarget[0].inputTargetGroup['+str(vBshId)+'].targetWeights['+str(vpId)+']', vVal)

def an_selectSetFromObj():
    vObg = an_getObj()
    vList = cmds.listAttr(vObg)
    attr=[]
    for vEach in vList:
        if "cPickleData" in vEach :
            attr.append(vEach)
    if len(attr)==1: an_loadSetFromObj(attr[0])
    else:
        if  cmds.window ("an_dialog", exists=True ): cmds.deleteUI ("an_dialog")
        cmds.window ("an_dialog", t="Select set window",  menuBar=True )
        cmds.columnLayout()
        cmds.text(l='Select set:')
        for vEach in attr:
            vRow = cmds.rowLayout(numberOfColumns=2,  )
            cmds.button(l=vEach.split("cPickleData")[1], c='an_loadSetFromObj("'+vEach+'" )', w=100 )
            cmds.button(l="del", c='an_delAttr("'+vEach+'" )', w=30 )
            cmds.setParent( '..' )
    cmds.showWindow ()


def an_delAttr(vMenuVal):
    vObg = an_getObj()
    cmds.deleteAttr(vObg+"."+vMenuVal)

def an_loadSetFromObj(vAttr):
    vObg = an_getObj()
    vString = cmds.getAttr  (vObg+"."+vAttr)
    vVert = cPickle.loads(str(vString))

    vChild = cmds.columnLayout("vButtonLayout", q= True , ca= True )
    for vI, vEach   in  enumerate(vChild):
        if vI>1: cmds.deleteUI (vEach)
    for vI, vEach   in  enumerate(vVert):
        vRow = cmds.rowLayout(numberOfColumns=100, p="vButtonLayout" ).split('|')[-1]
        cmds.text ( l= " "+str(vI+1)+" "  )
        cmds.button (l="add selected", c= 'addBut("'+vRow+'")')
        for vVertex in vEach:
            vNamber = vVertex.split('[')[1].split(']')[0]
            vButton = cmds.button (l= vNamber,   ann=vVertex, w=30 )
            cmds.button (vButton ,e=True , c= "an_buttonComand('"+vButton+"')" )
        cmds.setParent( '..' )

def an_selVertex():
    vSel = cmds.ls (sl=True, fl=True )
    cmds.scriptEditorInfo (writeHistory=True)
    Filename = cmds.scriptEditorInfo (q=True,  historyFilename=True )
    cmds.undoInfo (q=True,  pq=True )
    ListData = open(Filename).read().splitlines()[::-1]
    cmds.scriptEditorInfo (clearHistoryFile=True)
    cmds.scriptEditorInfo (writeHistory=False)
    vVertex = []
    for vString in  ListData[0:len(vSel)]:
         vVertex.append(vString.split(' ')[4])
    return vVertex[::-1]

def an_selSet():
    vData = an_getValUI( )
    vOut=[]
    for vlist in vData:
        for vVertex in vlist:
            vOut.append(vVertex)
    cmds.select ( vOut, r=True )

def an_recordToObg( ):
    vData = an_getValUI( )
    vObj=cmds.ls (sl=True)[0].split('.')[0]
    vAttrSuffix = cmds.textFieldGrp ("markFBG", query=True, text=True)
    if not vAttrSuffix: cmds.error( "-------->Add attribute name!")
    if not  mm.eval("attributeExists \"cPickleData"+vAttrSuffix+"\" "+vObj):
        cmds.addAttr   (vObj, ln= "cPickleData"+vAttrSuffix, dt="string", keyable = False)
    vString = cPickle.dumps(vData)
    cmds.setAttr (vObj+".cPickleData"+vAttrSuffix, vString, type="string" )

def an_getValUI( ):
    vChild = cmds.columnLayout("vButtonLayout", q= True , ca= True )
    vVertex=[]
    for  vEach   in  vChild [2:]:
        vPodChild = cmds.rowLayout(vEach, q= True , ca= True )
        vTemp=[]
        for  vEach   in  vPodChild [2:]:
            vTemp.append(cmds.button (vEach ,q=True , ann=True ))
        vVertex.append(vTemp)
    return vVertex

def an_vertexColumnUI(vButtonLayout):
    vChild = cmds.columnLayout(vButtonLayout, q= True , ca= True )
    for vI, vEach   in  enumerate(vChild):
        if vI>1: cmds.deleteUI (vEach)
    v_Rows = cmds.intSliderGrp ('rowISG1', q=True,  value=True )
    for i in range (0,v_Rows):
        an_vertexRowUI(i+1)

def an_vertexRowUI(vNamber):
    vRow = cmds.rowLayout(numberOfColumns=100, p="vButtonLayout" ).split('|')[-1]
    cmds.text ( l= " "+str(vNamber)+" "  )
    cmds.button (l="add selected", c= 'addBut("'+vRow+'")')
    cmds.setParent( '..' )

def addBut(vLayout):
    vChild = cmds.rowLayout(vLayout, q= True , ca= True )
    for vI, vEach   in  enumerate(vChild):
        if vI>1: cmds.deleteUI (vEach)
    vVert = an_selVertex()
    for vI, vEach   in  enumerate(vVert):
        vNamber = vEach.split('[')[1].split(']')[0]
        vButton = cmds.button (l= vNamber, p=vLayout, ann=vEach, w=30 )
        cmds.button (vButton ,e=True , c= "an_buttonComand('"+vButton+"')" )

def an_buttonComand(vBatName):
    vVal = cmds.radioButtonGrp('verRBG1', q=True, sl=True  )
    if vVal==1:
        print vBatName, "Add selected"
        vVert=cmds.ls(sl=True)[0]
        vert = cmds.button (vBatName ,e=True , ann=vVert, l= vVert.split('[')[1].split(']')[0])
    else:
        vert = cmds.button (vBatName ,q=True , ann=True )
        cmds.select (vert)


def an_getObj():
    if not cmds.ls(sl=True): cmds.error( "-------->Select object!")
    vObg = cmds.ls(sl=True)[0]
    if "." in vObg: vObg =vObg.split('.')[0]
    if cmds.objectType( vObg, isType='blendShape'): vObg = cmds.ls(sl=True, type="transform")[0]
    return vObg

def an_filTextfild():
    vChannelQuery =   cmds.channelBox ("mainChannelBox", q=True,  sha=True )[0]
    vBshQuery =  cmds.ls (sl=True)[0]
    cmds.textFieldButtonGrp ("bshTFBG", e=True, text= vBshQuery+'.'+vChannelQuery)






