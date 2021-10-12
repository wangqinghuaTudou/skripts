import PySide2
import shiboken2
from PySide2.QtWidgets import QWidget, QMenu
from maya.OpenMayaUI import MQtUtil

winPtr = MQtUtil.mainWindow()
mayaWindow = shiboken2.wrapInstance(long(winPtr), QWidget)

menubar = ""
for child in mayaWindow.children():
	if isinstance(child, PySide2.QtWidgets.QMenuBar):
		menubar = child

menu = QMenu("Helppppp")
menubar.addMenu(menu)


print (menubar)