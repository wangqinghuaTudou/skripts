#dobavil vozmoznost poiska i zameny
import maya.mel as mm
import maya.cmds as cmds

def  an_bshManager():

    win = "an_bshManager"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Blend shape manager.v02", rtf=True  )


    vCLayout =cmds.columnLayout()


    cmds.frameLayout( label='Rename, add preffix or sufix to target (selected in channel box):', borderStyle='etchedOut', bgc= [0, 0, 0], cll= True)
    cmds.separator (style="none", h=1  )
    vRCLayout = cmds.rowColumnLayout ( numberOfColumns=5, columnWidth=[(1, 90), (2, 90), (3, 90), (4, 90), (5, 90)])
    cmds.text (l="Input text:  ", align="right")
    cmds.textField ("textTF" )
    cmds.button (label='Add preffix', c="blendNameChange( \"prefix\")"  )
    cmds.button (label='Rename target', c="blendNameChange( \"rename\")"  )
    cmds.button (label='Add suffix', c="blendNameChange( \"sufix\")"  )
    cmds.setParent ('..');

    cmds.text (l="       Search and replace (do not forget select channel(s)):", align="left")

    vRCLayout = cmds.rowColumnLayout ( numberOfColumns=5, columnWidth=[(1, 90), (2, 90), (3, 90), (4, 90), (5, 90)])
    cmds.text (l="Search for:  ", align="right")
    cmds.textField ("SearchTF" )
    cmds.text (l="Replace withe:  ", align="right")
    cmds.textField ("ReplaceTF" )
    cmds.button (label='Apply', c="an_SearchAndReplace()"  )
    cmds.setParent( vCLayout)

    cmds.setParent( vCLayout)

    ###########
    cmds.frameLayout( label='Add In-between. Select target then base object:', borderStyle='etchedOut', bgc= [0, 0, 0], cll= True)
    cmds.separator (style="none", h=1  )
    cmds.rowColumnLayout ( numberOfColumns=5, columnWidth=[(1, 90), (2, 90), (3, 90), (4, 90), (5, 90)])
    cmds.text (l="Target index:  ", align="right")
    cmds.intField ("indexTF" )
    cmds.text (l="Weight:  ", align="right")
    cmds.floatField ("weightTF" )
    cmds.button (label='Add in-between', c="an_addInBetween( )" )
    cmds.setParent( vCLayout)
    ###########
    cmds.frameLayout( label='Replacement of the target. Select new target:', borderStyle='etchedOut', bgc= [0, 0, 0], cll= True)

    cmds.separator (style="none", h=1  )
    cmds.rowColumnLayout ( numberOfColumns=5, columnWidth=[(1, 90), (2, 90), (3, 90), (4, 90), (5, 90)])
    cmds.text (l="Target index:  ", align="right")
    cmds.intField ("indexTF2" )


    cmds.button (label='Add bsh node>>', c= "cmds.textField (\"BshTF\", e=True, text= cmds.ls (sl=True)[0])" )
    cmds.textField ("BshTF" )
    cmds.button (label='Connect target', c= "do_blndConnect ()" )
    cmds.setParent( vCLayout)

    cmds.showWindow (win)
###############################################################################################

def an_SearchAndReplace():

    if not cmds.ls (sl=True): cmds.error (" Please Select object and channel(s)")
    try: vObjQuery =  cmds.ls (sl=True, type="transform") [0]
    except IndexError: cmds.warning (" Please Select object and channel(s)")

    vBshQuery =  cmds.ls (sl=True ) [0]
    vChannelQuery =  cmds.channelBox ("mainChannelBox", q=True,  sha=True )
    vKeyQuery = cmds.textField ("SearchTF", q=True, tx=True )
    vInputQuery = cmds.textField ("ReplaceTF", q=True, tx=True )

    for vEach in vChannelQuery:
        cmds.aliasAttr (vEach.replace(vKeyQuery,vInputQuery), vBshQuery+"."+vEach)

######################

def do_blndConnect ():

    if not  cmds.ls (sl=True) : cmds.warning (" Please Select objects")
    vTarget =  cmds.listRelatives(cmds.ls (sl=True)[0], s=True)[0]
    vBshQuery = cmds.textField ("BshTF", q=True, tx=True )
    vIndexQuery = cmds.intField ("indexTF2", q=True, v=True )
    cmds.connectAttr   ( vTarget +".worldMesh[0]",   vBshQuery+".inputTarget[0].inputTargetGroup["+str(vIndexQuery)+"].inputTargetItem[6000].inputGeomTarget", f=True  )

def an_addInBetween():
    if not len(cmds.ls (sl=True)): cmds.warning (" Please Select objects")
    vTarget =  cmds.ls (sl=True)[0]
    vBase =  cmds.ls (sl=True)[1]
    vIndexQuery = cmds.intField ("indexTF", q=True, v=True )
    vWeightQuery = cmds.floatField ("weightTF", q=True, v=True )
    vList =  cmds.listHistory (vBase, pdo=True)
    vBlendShape =  cmds.ls (vList, type="blendShape") [0]
    cmds.blendShape (vBlendShape, e=True,  ib=True, t= (vBase, vIndexQuery,  vTarget, vWeightQuery))


def blendNameChange( vModQuery):# "rename", "prefix", "sufix"
    try: vNameQuery =  cmds.ls (sl=True) [0]
    except IndexError: cmds.warning (" Please Select object and bsh node")

    vChannelQuery =  cmds.channelBox ("mainChannelBox", q=True,  sha=True )
    vInputQuery = cmds.textField ("textTF", q=True, tx=True )
    try:
        if (vModQuery == "rename"):
            if (len(vChannelQuery) <= 1): cmds.aliasAttr (vInputQuery, vNameQuery+"."+vChannelQuery[0])

        if vModQuery == "prefix":
            for  objChannel in  vChannelQuery: cmds.aliasAttr (vInputQuery+objChannel, vNameQuery+"."+objChannel)

        if vModQuery == "sufix":
            for  objChannel in  vChannelQuery: cmds.aliasAttr (objChannel+vInputQuery, vNameQuery+"."+objChannel)
    except TypeError: cmds.warning (" Please Select one Atribute to Rename")

