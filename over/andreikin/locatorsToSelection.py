def locatorsToSelection():    
    selection = cmds.ls (sl=1)
    for sel in selection:
        loc = cmds.spaceLocator()[0]
        cmds.delete(cmds.parentConstraint( sel, loc, mo=False))