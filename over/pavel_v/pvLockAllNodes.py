import maya.cmds as mc

def pvLockAllNodes(isLock=True):
    allNodesList = mc.ls()
    if isLock:
        mc.lockNode(allNodesList, lock=True)
    else:
        mc.lockNode(allNodesList, lock=False)

# pvLockAllNodes()