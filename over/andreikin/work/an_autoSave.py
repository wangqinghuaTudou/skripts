#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''   an_autoSave   '''

import maya.cmds as cmds
import maya.api.OpenMaya as om
import  os, time
from an_Procedures.utilities import an_turnBasedUi
from threading import Timer,Thread,Event


global an_autoseveProcess, timer_object




TIME_TO_SAVE = 2


class perpetualTimer():
      def __init__(self,t,hFunction):
         self.t=t
         self.hFunction = hFunction
         self.thread = Timer(self.t,self.handle_function)

      def handle_function(self):
         self.hFunction()
         self.thread = Timer(self.t,self.handle_function)
         self.thread.start()

      def start(self):
         self.thread.start()

      def cancel(self):
         self.thread.cancel()


def an_autoSave(): 
    global an_autoseveProcess
    leauts = an_turnBasedUi('skn', title ='Auto save manager  v 1.00',  stepsLabel =["Default auto save path:",  ])
    cmds.intSliderGrp('d_timeISG', field=True, label='Save every:       ', minValue=1, maxValue=30, fieldMinValue=1, fieldMaxValue=100, value=TIME_TO_SAVE, p=leauts[0] )
    lb, cl = ['Stop', [1, 0, 0]] if an_autoseveProcess else  ["Start", [0.4, 0.4, 0.4] ]
    cmds.button ('procB', l=lb, c="do_save()", bgc=cl,  p=leauts[0])


def switch_ui():
    global an_autoseveProcess
    #an_autoseveProcess = True if cmds.button ('procB', q=1, l=1)=='Start' else False
    
    lb, cl = ['Stop', [1, 0, 0]] if an_autoseveProcess else  ["Start", [0.4, 0.4, 0.4] ]
    cmds.button ('procB', e=1, l=lb, c="action()", bgc=cl)



def do_save():
    timer_object.cancel()
    print ('avtorig act')
    




if not 'an_autoseveProcess' in globals(): an_autoseveProcess = True
timer_object = perpetualTimer(TIME_TO_SAVE, do_save)
timer_object.start()


an_autoSave()

#path = os.path.dirname(maya.cmds.file(q=True, sn=True))
#om.MGlobal.displayWarning('The argument must be 0 or 1.')











 



