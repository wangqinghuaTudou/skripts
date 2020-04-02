import maya.cmds as mc
import re

def pvRename():
    prefixList = ['none', \
                  'l_', \
                  'r_', \
                  'up_', \
				  'fv_', \
				  'bk_', \
                  'lo_', \
                  'mid_']
    suffixList = ['none', \
                  '_CT', \
                  '_bind', \
                  '_jnt', \
                  '_geo', \
                  '_grp', \
                  '_crv', \
                  '_clstr', \
                  '_loc', \
                  '_mdv', \
                  '_pma', \
                  '_uc', \
                  '_mdl', \
                  '_adl', \
                  '_flcl']

    if mc.window('pvRename_ui', exists=True):
        mc.deleteUI('pvRename_ui')
    mc.window('pvRename_ui', \
              sizeable=False, \
              width=150, \
              height=100, \
              title='Rename Objects')

    mc.columnLayout(adjustableColumn=True)
    mc.separator(height=3, style='none')
    mc.rowColumnLayout(numberOfColumns=4, \
                       columnAttach=[1, 'left', 20], \
                       columnWidth=[[1, 90], [2, 150], [3, 50], [4, 80]])
    mc.text(align='left', label='Prefix:')
    mc.text(align='left', label='Name:')
    mc.text(align='left', label='Digits:')
    mc.text(align='left', label='Suffix:')
    mc.setParent('..')

    mc.columnLayout(adjustableColumn=True)
    mc.rowColumnLayout(numberOfColumns=4, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[1, 80], [2, 150], [3, 50], [4, 80]])
    mc.optionMenuGrp('pvRenPrefOptMenGrp', columnWidth=[1, 50])
    for item in prefixList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('pvRenPrefOptMenGrp', edit=True, select=2)
    mc.textField('pvRenNameTexFld', text='')
    mc.textField('pvRenDigTexFld', text='##')
    mc.optionMenuGrp('pvRenSuffOptMenGrp', columnWidth=[1, 50])
    for item in suffixList:
        mc.menuItem(label=item)
    mc.optionMenuGrp('pvRenSuffOptMenGrp', edit=True, select=2)
    mc.setParent('..')

    mc.columnLayout(adjustableColumn=True)
    mc.separator(height=5, style='in')
    mc.rowColumnLayout(numberOfColumns=3, \
                       columnAttach=[1, 'left', 10], \
                       columnWidth=[[1, 100], [2, 155], [3, 80]])
    mc.radioCollection('pvRenRadCol')
    mc.radioButton('pvRenRadButtSel', label='Selected')
    mc.radioButton('pvRenRadButtHier', label='Hierarchy')
    mc.radioCollection('pvRenRadCol', edit=True, select='pvRenRadButtSel')
    mc.button('pvRenRunButt', \
           label='OK', \
           width=80, \
           command='pvRenameMain()')

    mc.showWindow('pvRename_ui')

def pvRenameMain():
    prefix = mc.optionMenuGrp('pvRenPrefOptMenGrp', query=True, value=True)
    if prefix == 'none':
        prefix = ''
    newName = mc.textField('pvRenNameTexFld', query=True, text=True)
    digits = mc.textField('pvRenDigTexFld', query=True, text=True)
    numDigits = digits.count('#')
    if numDigits == 0:
        print 'Count of # must be more then 0.'
        return
    substr = '#' * numDigits
    zeroSubstr = '0' * numDigits
    newDig = digits.replace(substr, zeroSubstr)
    if newDig == digits:
        print 'Digits must contain only # symbols.'
        return
    digs = digits.replace(substr, '%0' + str(numDigits) + 'd')
    suffix = mc.optionMenuGrp('pvRenSuffOptMenGrp', query=True, value=True)
    if suffix == 'none':
        suffix = ''

    sel = mc.ls(selection=True)
    if not sel:
        print 'Must be selected at least one object.'
        return
    else:
        node = mc.createNode('unknown')
        mc.addAttr(node, longName='selObjects', attributeType='message', multi=True, indexMatters=False)
        for each in sel:
            mc.connectAttr('%s.message'%each, '%s.selObjects'%node, nextAvailable=True)
            if mc.radioButton('pvRenRadButtHier', query=True, select=True):
                pvFindChildren(each, node)

        con = mc.listConnections('%s.selObjects'%node, source=True, destination=False)
        for i, obj in enumerate(con):
            num = i + 1
            objCurr = mc.listConnections('%s.selObjects[%s]'%(node, i))[0]
            newDigs = (digs % num)
            result = prefix + newName + newDigs + suffix
            mc.select(objCurr, replace=True)
            result = mc.rename(result)
        mc.delete(node)
        mc.select(clear=True)

def pvFindChildren(parent, node):
    children = mc.listRelatives(parent, children=True, fullPath=True)
    if children:
        for child in children:
            mc.connectAttr('%s.message'%child, '%s.selObjects'%node, na=True)
            pvFindChildren(child, node)

