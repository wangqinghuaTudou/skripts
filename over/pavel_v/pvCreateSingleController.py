'''
    Script:             pvCreateSingleController.py

    Author:             Pavel Volokushin
    Mail:               p.volokushin@gmail.com
    
    Release date:       07.08.2015
    Current version:    1.0
    Last change:        none

    Usage:              Execute command in command line
                        pvCreateSingleController()
                        Then enter controller's name in text field and press "Create" button or hit "Enter" key

    Description:        Create single controller with "*_con" group above it for connections and "*_ori" locator for 
                        controller's orientation. Also create single "*_bind" joint as child of controller to bind
                        it to any object.

    Return:             none
    Files needed:       none
'''


import maya.cmds as mc

def pvCreateSingleController():

    mainWindow = 'pvCreateCtWindow'
    mainLayout = 'pvCreateCtMainColumnLayout'
    nameText = 'pvCtNameText'
    nameTextField = 'pvCtNameTextField'
    nameExecuteButton = 'pvCtNameExecuteButton'

    if mc.window(mainWindow, exists=True):
        mc.deleteUI(mainWindow)

    mc.window(mainWindow, \
              sizeable=False, \
              width=210, \
              height=50, \
              title='Create Controller')

    mc.columnLayout(mainLayout, adjustableColumn=True)
    mc.text(nameText, label='Create Single CT with Name: ', align='left')
    mc.textField(nameTextField, width=100, enterCommand='pvCreateSingleControllerMain()')
    mc.button(nameExecuteButton, label='Create', command='pvCreateSingleControllerMain()')

    mc.showWindow(mainWindow)

def pvCreateSingleControllerMain():

    nameTextField = 'pvCtNameTextField'
    mainControllerName = mc.textField(nameTextField, query=True, text=True)
    oriLocatorName = mainControllerName + '_ori'
    conGroupName = mainControllerName + '_con'
    controllerName = mainControllerName + '_CT'
    controlelrShapeName = controllerName + 'Shape'
    jointName = mainControllerName + '_bind'

    mc.spaceLocator(name=oriLocatorName, position=[0, 0, 0])
    mc.group(name=conGroupName, world=True, empty=True)
    mc.circle(name=controllerName, center=[0, 0, 0], normal=[0, 1, 0], sweep=360, radius=1, degree=3, useTolerance=0, tolerance=0.01, sections=8, constructionHistory=0)
    if mc.objExists(controlelrShapeName + '.overrideEnabled'):
        mc.setAttr(controlelrShapeName + '.overrideEnabled', 1)
        mc.setAttr(controlelrShapeName + '.overrideColor', 17)
        
    mc.joint(name=jointName)
    mc.parent(conGroupName, oriLocatorName)
    mc.parent(controllerName, conGroupName)
    
    mc.select(oriLocatorName, replace=True)

#pvCreateSingleController()