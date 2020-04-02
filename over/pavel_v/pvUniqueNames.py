import maya.cmds as cmds
import maya.OpenMaya as om
import re

class UniqueNames(object):

    def __init__(self):
        pass

    def fixNonUniqueName(self, name, hashes='##'):
        nHash = hashes.count('#')
        currentNumber = re.findall('(\d+)', name)
        newDigits = ('%0' + str(nHash) + 'd')
        nameParts = name.split('_')

        if currentNumber:
            currentNumber = currentNumber[0]
            numberIncrement = int(currentNumber)
            newNumber = (newDigits % numberIncrement)
            newName = name.replace(currentNumber, newNumber)
            while cmds.objExists(newName):
                numberIncrement += 1
                newNumber = (newDigits % numberIncrement)
                newName = name.replace(currentNumber, newNumber)
        elif len(nameParts) > 1:
            mainName = nameParts[0]
            if len(nameParts) > 2:
                for part in nameParts[1:-1]:
                    mainName = mainName + '_' + part
            numberIncrement = 1
            newNumber = (newDigits % numberIncrement)
            newName = mainName + newNumber + '_' + nameParts[-1]
            while cmds.objExists(newName):
                numberIncrement += 1
                newNumber = (newDigits % numberIncrement)
                newName = mainName + newNumber + '_' + nameParts[-1]
        else:
            numberIncrement = 1
            newNumber = (newDigits % numberIncrement)
            newName = name + newNumber
            while cmds.objExists(newName):
                numberIncrement += 1
                newNumber = (newDigits % numberIncrement)
                newName = name + newNumber
        return newName

    def fix(self, type):
        self.nodes = []
        self.scanReport = ''
        self.fixReport = ''
        nonUniqueList = []
        dagObjects = cmds.ls(dagObjects=True, type=type)

        if dagObjects:
            for dag in dagObjects:
                if '|' in dag:
                    nonUniqueList.append(dag)
        if nonUniqueList:
            for nonUnq in nonUniqueList:
                namePathParts = nonUnq.split('|')
                self.nodes.append(nonUnq)
                self.scanReport += '%s\n' % namePathParts[-1]
            om.MGlobal.displayInfo('---------------------------------------')
            om.MGlobal.displayInfo('Scan report:')
            om.MGlobal.displayInfo(self.scanReport)
        else:
            om.MGlobal.displayInfo('---------------------------------------')
            om.MGlobal.displayInfo('Scene has\'t any non unique names.')
        if self.nodes:
            for node in self.nodes:
                namePathParts = node.split('|')
                name = str(namePathParts[-1])
                newName = self.fixNonUniqueName(name)
                cmds.rename(node, newName)
                self.fixReport += '%s\n' % newName
            om.MGlobal.displayInfo('---------------------------------------')
            om.MGlobal.displayInfo('Fix report:')
            om.MGlobal.displayInfo(self.fixReport)

a = UniqueNames()
a.fix('transform')
a.fix('shape')