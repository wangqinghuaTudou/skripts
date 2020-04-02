import maya.cmds as mc
import pvProcedures as pvp
import CharacterNames as chnm

def pvSelectAllBodyControllers():
    namespace = pvp.pvGetNameSpaces()
    charNames = chnm.CharacterNames()
    allBodyCt = charNames.getWholeBody()
    mc.select(clear=True)
    for ct in allBodyCt:
        ctName = namespace[0] + ct
        if mc.objExists(ctName):
            mc.select(ctName, add=True)