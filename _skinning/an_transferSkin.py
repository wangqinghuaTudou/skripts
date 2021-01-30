import maya.cmds as cmds
from  anProcedures import  *
from an_skinProcedures import  *
import copy

def an_transferSkin():                                                                              # user interface
    vWin = "an_transferSkinUI"
    vWinHight = 150
    if cmds.window (vWin, exists=True): cmds.deleteUI ( vWin, window=True )
    cmds.window  (vWin, t="Transfer skin  v 1.00", sizeable=False, wh= [432, vWinHight], menuBar=True )

    cmds.menu (label="Addition"  )
    cmds.menuItem( label='Load set', c= 'loadSaveSet("load")')
    cmds.menuItem( label='Save set', c= 'loadSaveSet("save")')
    cmds.menuItem( label='Load preset', c= 'loadPreSet()')    
    cmds.columnLayout( )
    cmds.separator   (h=2 )
    cmds.frameLayout( label='Working geometry:',  lv=True, backgroundColor=[ 0, 0, 0 ], w= 427, marginWidth = 2)
    cmds.columnLayout(backgroundColor=[ 0.3, 0.3, 0.3 ])
    cmds.textFieldButtonGrp ('TFBG_SkinGeo', l="Skin geo :   ",  bl=" Add selected",  cw = [(1, 124), (2, 170)],  bc = "cmds.textFieldButtonGrp ('TFBG_SkinGeo', e=1, tx= cmds.ls (sl=1)[0])" )
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 213), (2, 214)],  columnSpacing=[(2,2),(3,2)] )
    cmds.button( label='Replace twist from skin', command= 'delTwFromSkin()', backgroundColor=[ 0.4, 0.4, 0.4 ])
    cmds.button( label='Add twist to skin claster', command= "addTwToSkin()", backgroundColor=[ 0.4, 0.4, 0.4 ])
    cmds.setParent ('..')
    cmds.frameLayout('addLayout', label='           Twist geometry:                         Skin joint/geometry: ',  lv=True, backgroundColor=[ 0, 0, 0 ], w= 427, marginWidth = 2)
    cmds.setParent ('..')
    cmds.separator   (h=5 )
    cmds.button( label='Add couple', command= "an_twistUiBlock()", backgroundColor=[ 0.4, 0.4, 0.4 ], w= 213,)
    cmds.showWindow( vWin )
    cmds.window  (vWin,e=True,  wh=[432, vWinHight])

def loadSaveSet (act):
    if act=='load':
        skinGeo= cmds.ls (sl=1)[0]
        data = an_saveLoadData(obgect=skinGeo)
        cmds.textFieldButtonGrp ('TFBG_SkinGeo', e=1, tx= skinGeo)

        for twGeo, skinJnt in data:
            cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )+31 )
            layoutR = cmds.rowColumnLayout( numberOfColumns=6, columnWidth=[(1, 140), (2, 40), (3, 140), (4, 40), (5, 50)],  columnSpacing=[(4,2),(3,2)],  p='addLayout' )
            textFild = cmds.textField(text = twGeo)
            bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
            cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
            textFild = cmds.textField(text = skinJnt)
            bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
            cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
            bc1 = 'cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )-31 );'
            bc2 = 'cmds.deleteUI("'+layoutR+'")'
            cmds.button(l='delete',  backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc1+bc2)
            cmds.setParent( '..')
        #print data
    if act=='save':
        skinGeo = cmds.textFieldButtonGrp ('TFBG_SkinGeo', q=True,tx=True)
        output = []
        for eachLayout in cmds.frameLayout('addLayout', q=True, ca=True ):
            txtLayouts = cmds.rowColumnLayout(eachLayout, q=True, ca=True )
            twGeo = cmds.textField(txtLayouts[0], q=True, tx=True )
            skinJnt = cmds.textField(txtLayouts[2], q=True, tx=True )
            output.append([twGeo, skinJnt, ])
        print output
        an_saveLoadData(data=output, obgect=skinGeo) #save and load data to/from object and file


def loadPreSet ():

    data= [ [u'neckTwTw_geo', u'neck_bind'], 
            [u'l_armBendUpTw_geo', u'l_upArm_jnt'], 
            [u'l_armBendDwTw_geo', u'l_foreArm_jnt'], 
            [u'r_armBendUpTw_geo', u'r_upArm_jnt'], 
            [u'r_armBendDwTw_geo', u'r_foreArm_jnt'], 
            [u'bodyTwTw_geo', u'bodyTwTw_geo'], 
            [u'l_legBendUpTw_geo', u'l_upLeg_jnt'], 
            [u'l_legBendDwTw_geo', u'l_lowLeg_jnt'], 
            [u'r_legBendUpTw_geo', u'r_upLeg_jnt'], 
            [u'r_legBendDwTw_geo', u'r_lowLeg_jnt']] # 

    for twGeo, skinJnt in data:
        cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )+31 )
        layoutR = cmds.rowColumnLayout( numberOfColumns=6, columnWidth=[(1, 140), (2, 40), (3, 140), (4, 40), (5, 50)],  columnSpacing=[(4,2),(3,2)],  p='addLayout' )
        textFild = cmds.textField(text = twGeo)
        bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
        cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
        textFild = cmds.textField(text = skinJnt)
        bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
        cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
        bc1 = 'cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )-31 );'
        bc2 = 'cmds.deleteUI("'+layoutR+'")'
        cmds.button(l='delete',  backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc1+bc2)
        cmds.setParent( '..')

def an_twistUiBlock( ): # ui which  is inserted to global ui for the each target
    cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )+31 )
    layoutR = cmds.rowColumnLayout( numberOfColumns=6, columnWidth=[(1, 140), (2, 40), (3, 140), (4, 40), (5, 50)],  columnSpacing=[(4,2),(3,2)],  p='addLayout' )
    textFild = cmds.textField()
    bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
    cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
    textFild = cmds.textField()
    bc = 'cmds.textField("'+textFild+'", e=True, tx=cmds.ls(sl=True)[0])'
    cmds.button(l='add ',   backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc  )
    bc1 = 'cmds.window ("an_transferSkinUI",e=True, height=cmds.window ("an_transferSkinUI",q=True, height=True )-31 );'
    bc2 = 'cmds.deleteUI("'+layoutR+'")'
    cmds.button(l='delete',  backgroundColor=[ 0.4, 0.4, 0.4 ], c = bc1+bc2)
    cmds.setParent( '..')


def an_getListUi( ):
    skinGeo = cmds.textFieldButtonGrp ('TFBG_SkinGeo', q=True,tx=True)
    output = []

    for eachLayout in cmds.frameLayout('addLayout', q=True, ca=True ):
        txtLayouts = cmds.rowColumnLayout(eachLayout, q=True, ca=True )
        twGeo = cmds.textField(txtLayouts[0], q=True, tx=True )
        skinJnt = cmds.textField(txtLayouts[2], q=True, tx=True )
        twistClusterName =  cmds.ls (cmds.listHistory (twGeo, pdo=1), type='skinCluster')[0]    ### if claster sel

        #cmds.setAttr (skinClusterName + ".envelope", 0)
        skinGeoCopy = cmds.duplicate(skinGeo)[0]             #  Copy skin geo and skin copy from tw jnt
        twJoint = cmds.ls (cmds.listHistory (twistClusterName, levels=1), type='transform')  ###   jnt tw
        copySkinClaster = cmds.skinCluster(skinGeoCopy,  twJoint,  tsb=True,  ug=True, dr=4, ps=False,  rui=False,  mi=5,  omi=False,  nw=True)[0]
        cmds.copySkinWeights( sourceSkin=twistClusterName, destinationSkin=copySkinClaster, noMirror=True, sa="closestPoint" )
        jntTwWeightDic = getSkin(skinGeoCopy)     # get twist weiht for each couple
        cmds.skinCluster(copySkinClaster,   e=True, ub=True )
        cmds.delete (skinGeoCopy)
        output.append([twGeo, skinJnt, jntTwWeightDic])
        #cmds.setAttr (skinClusterName + ".envelope", 1)
    return output

#______________________________________________________________________________________

def delTwFromSkin ():

    objList = an_getListUi()                                                              # get  couples - twGeo and jnt
    skinGeo = cmds.textFieldButtonGrp ('TFBG_SkinGeo', q=True,tx=True)                    # skin geo name
    jntWeightDic = getSkin(skinGeo)                                           # get skin jnt and weight list
    skinClusterName =  cmds.ls (cmds.listHistory (skinGeo, pdo=1), type='skinCluster')[0] # claster
    pIdList = range(cmds.getAttr (skinGeo + ".cp", size=True ))

    twJntAll =[]
    for list in  [data[2].keys() for data in objList] : twJntAll=twJntAll+list # get all tw joints

    out = {}
    for jnt in jntWeightDic.keys():
        if not jnt in  twJntAll : # set weight for over join
            out[jnt] = jntWeightDic[jnt]

    out.keys()

    for twistGeo, skinJnt, jntTwWeightDic in  objList : #           # for each caple
        rez = []
        for pId in pIdList:

            summa  = sum ([ jntWeightDic[jnt][pId] for jnt in jntTwWeightDic.keys()])
            rez.append (summa)
        out[skinJnt] = rez

    cmds.skinCluster(skinClusterName,   e=True, ub=True )
    setSkin ( skinGeo,  out )
    print ""


#______________________________________________________________________________________

def addTwToSkin ():
    objList = an_getListUi()                                                              # get  couples - twGeo and jnt

    skinGeo = cmds.textFieldButtonGrp ('TFBG_SkinGeo', q=True,tx=True)                    # skin geo name
    jntWeightDic = getSkin(skinGeo)                                           # get skin jnt and weight list
    skinClusterName =  cmds.ls (cmds.listHistory (skinGeo, pdo=1), type='skinCluster')[0] # claster
    pIdList = range(cmds.getAttr (skinGeo + ".cp", size=True ))                           # list of point id

    out = {}
    for jnt in jntWeightDic.keys():
        if not jnt in  [ objList[x][1] for x in  range(len(objList))] : # set weight for over join
            print  jnt
            out[jnt] = jntWeightDic[jnt]

    for twistGeo, skinJnt, jntTwWeightDic in  objList :       #print twistGeo, skinJnt, jntTwWeightDic.keys()
        for twJnt in jntTwWeightDic.keys():
            rez = []
            for pId in range (len (pIdList)):
                rez.append( jntWeightDic [skinJnt][pId]* jntTwWeightDic[twJnt][pId] )
            out[twJnt]= rez

    cmds.skinCluster(skinClusterName,   e=True, ub=True )
    setSkin ( skinGeo,  out )
    print ""




