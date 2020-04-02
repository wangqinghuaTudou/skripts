import maya.cmds as mc
import maya.OpenMaya as mo

def pvDeleteUnusedCameras(*args):

    deletedCamerasList = []

    if not args:
        args = mc.ls(selection=True)
    if not args:
        mo.MGlobal.displayInfo('Must be selected any camera(s) or group of cameras or both.')
    else:
        for obj in args:
            allDescCameras = mc.listRelatives(obj, allDescendents=True, type='camera', fullPath=True)
            if allDescCameras:
                for ad in allDescCameras:
                    mc.camera(ad, edit=True, startupCamera=False)
                for ad in allDescCameras:
                    try:
                        cameraParent = mc.listRelatives(ad, parent=True, fullPath=True)
                        mc.delete(cameraParent[0])
                        deletedCamerasList.append(cameraParent[0])
                    except:
                        pass

    mo.MGlobal.displayInfo('Cameras were successfully deleted: %s'%deletedCamerasList)
    return deletedCamerasList