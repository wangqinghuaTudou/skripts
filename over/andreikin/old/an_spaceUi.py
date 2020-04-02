import maya.cmds as cmds
from CharacterNames import CharacterNames as CName
from An_Space import An_Space as An_Space

def an_tatgetUiBlock( target, attr): # ui which  is inserted to global ui for the each target
    cmds.window ("spaceUi",e=True, height=cmds.window ("spaceUi",q=True, height=True )+25 )
    cmds.rowColumnLayout(target+'Layout', nc =4 ,  p='spaceTargetColumnLayout'  )
    cmds.text ( '' , al='left',  width= 142  )
    cmds.textField(target+'textField', tx= target)
    cmds.textField(target+'attrField', tx=attr )
    butCom = 'cmds.deleteUI("'+target+'Layout");'+'cmds.window ("spaceUi",e=True, height=cmds.window ("spaceUi",q=True, height=True )-25 )'
    cmds.button(l='delete', c=butCom ,w=62 )
    cmds.setParent( '..')
                                                                     # insert all target and atributes to Ui
def an_addTargetsToUI(): [an_tatgetUiBlock( target, CName(target).divideName()[0]+CName(target).divideName()[1]) for  target in cmds.ls(sl=True)]

def an_deleteSpace():
    controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True, )
    spaceType = {1:'parent', 2:"point", 3:"orient"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    classObj = An_Space(controller, spaceType = spaceType )
    classObj.delSpaceObj()
    #cmds.deleteAttr (controller, attribute=classObj.attrDic[classObj.spaceType])
    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:  #del targets ui
        cmds.deleteUI (Layout)
        cmds.window ("spaceUi",e=True, height=cmds.window ("spaceUi",q=True, height=True )-25 )

def an_insertSpaceToUi( fromTextFild = True):  # fill interface after specifying controller or type
    if fromTextFild :
        controller =  cmds.ls (sl=True)[0]
        cmds.textFieldButtonGrp ('TFBG_control', e=True, tx=controller )
    else: controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True )
    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:
            cmds.deleteUI (Layout)
            cmds.window ("spaceUi",e=True, height=cmds.window ("spaceUi",q=True, height=True )-25 )
    spaceType = {1:'parent', 2:"point", 3:"orient"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    classObj = An_Space( controller, spaceType = spaceType )
    if cmds.objExists(controller+'.'+classObj.attrDic[spaceType]):
        info = classObj.getSpaceInfo( controller+'.'+classObj.attrDic[spaceType])
        cmds.textFieldButtonGrp ('TFBG_object', e=True, tx=info[0] )
        for target in info[1] : an_tatgetUiBlock( target[0], target[1])


def an_spaceUi():# sozdaet interfase
    win = "spaceUi"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t="Space maker v3.00", width=440,  height=169, s=False, rtf=True, menuBar=True )
    cmds.window ("spaceUi", e=True,  height=169 )
    cmds.columnLayout ('spaceColumnLayoutName'  , adjustableColumn=True)
    cmds.frameLayout( label='Base and control objects:', bgc =[0,0,0] )
    cmds.columnLayout (  adjustableColumn=True)
    cmds.textFieldButtonGrp ('TFBG_control', l="Controler:",  bl="<<Add selected",
            cw = [(1, 124), (2, 210)],  bc = "an_insertSpaceToUi()" )
    cmds.textFieldButtonGrp ('TFBG_object', l="Objects:",  bl="<<Add selected",
            cw = [(1, 124), (2, 210)],  bc = "cmds.textFieldButtonGrp ('TFBG_object', e=True, tx=  cmds.ls (sl=True)[0])" )
    cmds.radioButtonGrp('typeRBG', label='Constraint type:  ',
                        labelArray3=['Parent', 'Point', 'Orient'],
                        numberOfRadioButtons=3,
                        sl=1,
                        cw = [(1, 130), (2, 110)],
                        cc = "an_insertSpaceToUi(fromTextFild = False)" )
    cmds.setParent( 'spaceColumnLayoutName')

    cmds.frameLayout( label='Targets and attributes:', bgc =[0,0,0] )
    cmds.columnLayout ('spaceTargetColumnLayout'  ,  adjustableColumn=True)
    cmds.rowColumnLayout(nc =4 ,  p='spaceTargetColumnLayout'  )
    cmds.text ( '' , al='left',  width= 142  )
    cmds.text ( '  target:' , al='left', width= 122  )
    cmds.text ( 'attribut:' , al='left' , width= 142 )
    for i in (0,1):  cmds.setParent( '..')

    cmds.rowColumnLayout(nc =3   )
    cmds.button(l='Add selectet targets', c='an_addTargetsToUI()',w=142 )
    cmds.button(l='Delete space', c='an_deleteSpace()',w=142 )
    cmds.button(l='Make / Edit space', c='makeEditSpace()',w=142 )
    cmds.showWindow()

def makeEditSpace():
    controller = cmds.textFieldButtonGrp ('TFBG_control', q=True, tx=True)
    object = cmds.textFieldButtonGrp ('TFBG_object', q=True, tx=True)
    spaceType = {1:'parent', 2:"point", 3:"orient"}[cmds.radioButtonGrp('typeRBG', q=True,  sl=True )]
    targetList=[]

    for Layout in cmds.columnLayout ('spaceTargetColumnLayout',  q=True, ca=True)[1:]:
        filds = cmds.rowColumnLayout (Layout,  q=True, ca=True)[1:]
        targetList.append([cmds.textField(filds[0], q=True, tx=True), cmds.textField(filds[1], q=True, tx=True)])

    classObj = An_Space( controller, object, targetList, spaceType=spaceType)
    classObj.rebildSpaceObj()









