#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, cPickle
import maya.mel as mm
"""
1 Переключатель рендер / динам. версия
2 Формирование списков пар под проэкт.
3 Редактирование списков пар под проэкт.
4 Интерфейс.

"""

FILE = 'D:/work/malysh.dat'
GLOB_DIC = {}

def addChar(): 
    car_Name = cmds.fileDialog2( fileMode=1, caption="Load render varsion", dir=os.path.dirname(FILE) )[0]
    carMid_Name = cmds.fileDialog2( fileMode=1, caption="Load dynamic varsion", dir=os.path.dirname(FILE) )[0]
    GLOB_DIC[car_Name]=carMid_Name

def loadInfo(FILE):
    global GLOB_DIC
    r = open(FILE, 'r')
    GLOB_DIC = cPickle.load(r)
    r.close()

def getCharlist(dynVer = False):
    charlist =[]
    for elem in  GLOB_DIC.keys():
        if not dynVer :
            charlist.append(os.path.basename(elem).split(".")[0])
        else:
            charlist.append(os.path.basename(GLOB_DIC[elem]).split(".")[0])
    return charlist

def saveInfo(FILE):
    f = open(FILE, 'w')
    cPickle.dump(GLOB_DIC , f )
    f.close()
    
def scenCharlist():
    refNodes = mm.eval('ls -type reference')
    cmds.referenceQuery('massovka_barsik:general_CT ',filename=True )


