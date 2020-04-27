#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, cPickle
import maya.mel as mm
import maya.cmds as cmds
"""
1 Переключатель рендер / динам. версия
2 Формирование списков пар под проэкт.
3 Редактирование списков пар под проэкт.
4 Интерфейс.

"""

FILE = 'D:/work/Project/dynChar.dat'
GLOB_DIC = {}
SFX='rmanager'

def refManadjer(): 

    WIDTH =420
    win = SFX+"Win"
    if  cmds.window (win, exists=True ): cmds.deleteUI (win)
    cmds.window (win, t='', width=WIDTH,  height=10, s=False, rtf=True, menuBar=True )
    cmds.scrollLayout
    cmds.columnLayout (SFX+"ColumnL", adjustableColumn=True)
    cmds.frameLayout (  label="Referens manager"   , cll=0, w=WIDTH , bgc=[0,0,0], borderVisible=True)
    cmds.textFieldButtonGrp(SFX+"pathF", label='Path :  ', text=FILE, buttonLabel='   Change project  ', columnWidth3=[WIDTH*0.2, WIDTH*0.55, WIDTH*0.6], bc='changeDir()' )
    cmds.rowColumnLayout( numberOfColumns=4 , columnWidth=[(1, WIDTH/4), (2, WIDTH/4), (3, WIDTH/4), (4, WIDTH/4)], cs=([2, 1] ,[3, 1],[4, 1]) )
    cmds.button(  l="add char", c="addChar()" )
    cmds.button(  l="del char", c="deelChar()"  )
    cmds.button(  l="make new file", c="newFile()" )
    cmds.button(  l="print charlist", c="printChars()"  )
    cmds.setParent( ".." )
    cmds.button(  l="Swap", c="swapSel()"  )
    cmds.showWindow (win)
    cmds.window (win, e=True,  height=120 )

def newFile():
    global FILE, GLOB_DIC
    FILE = cmds.fileDialog2(fileFilter='*.dat', fileMode=0, caption="Save position" )[0]
    GLOB_DIC = {}
    f = open(FILE, 'w')
    cPickle.dump(GLOB_DIC , f )
    f.close()
    cmds.textFieldButtonGrp(SFX+"pathF", e=True, text=FILE)

def changeDir():
    global FILE
    dir_Name = cmds.fileDialog2( fileMode=1, caption="Add new path", dir=os.path.dirname(FILE))[0]
    FILE = dir_Name
    cmds.textFieldButtonGrp(SFX+"pathF", e=True, text=FILE)
    
def addChar(): 
    global FILE
    char_Name = cmds.fileDialog2( fileMode=1, caption="Load render varsion", dir=os.path.dirname(FILE) )[0]
    charMid_Name = cmds.fileDialog2( fileMode=1, caption="Load dynamic varsion", dir=os.path.dirname(FILE) )[0]
    GLOB_DIC[char_Name]={'midVer':charMid_Name, 'name':os.path.basename(char_Name).split(".")[0]}
    saveInfo(FILE)
    print  char_Name, ' is added'
    
def delChar():
    global GLOB_DIC
    loadInfo(FILE)
    GLOB_DIC.pop( cmds.fileDialog2( fileMode=1, caption="Load render varsion", dir=os.path.dirname(FILE))[0])
    saveInfo(FILE)

def loadInfo(FILE):
    global GLOB_DIC
    r = open(FILE, 'r')
    GLOB_DIC = cPickle.load(r)
    r.close()

def saveInfo(FILE):
    f = open(FILE, 'w')
    cPickle.dump(GLOB_DIC , f )
    f.close()

def printChars():
    print '\n\n\n'
    loadInfo(FILE)
    for ch in GLOB_DIC.keys():
        print GLOB_DIC[ch]['name'], ' --- ', ch, ' --- ', GLOB_DIC[ch]['midVer']

def swapSel():
    selLen = len(cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True ).split('.m')[0])+3
    selRef = cmds.referenceQuery(cmds.ls(sl=True)[0],filename=True )[:selLen]
    loadInfo(FILE)
    refNod  =  cmds.referenceQuery(cmds.ls(sl=True)[0],referenceNode=True )

    if selRef in GLOB_DIC.keys():
        cmds.file(GLOB_DIC[selRef]['midVer'] , loadReference= refNod)
    else: 
        cmds.error('There is no such character in the list!')


 
 





