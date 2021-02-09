from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import re
import functools
import logging

ABOUT_SCRIPT = "\n" \
               "Latest updates:                \n" \
               "3.02.2021    -start writing    \n" \
               "                               \n" \
               "Created by Andrey Belyaev      \n" \
               "andreikin@mail.ru"

HELP_LABEL = "Select the required character controller and click bake dynamics. \n" \
             "After baking, you can fix problem points manually. "

HELP_TEXT = "\n" \
            "1 Choose the character you want to work with by choosing one of his controllers.\n" \
            "2 If you need to cache one dynamic system, click 'Bake_selaction'\n" \
            "3 To cache all dynamic systems, choose 'Bake_all'\n" 


class BakeStrand(QMainWindow):
    def __init__(self):
        super(BakeStrand, self).__init__()
        # Window
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Bake strand system")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.__menu_bar()  # help and About script windows
        self.__label()  # text on top
        self.__buttons()

    def __menu_bar(self):
        menuBar = QMenuBar()
        self.setMenuBar(menuBar)
        menu = QMenu("Help")
        menuBar.addMenu(menu)
        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(functools.partial(self.text_dialog, "Help"))
        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(functools.partial(self.text_dialog, "About program"))

    def __label(self):
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)

    def __buttons(self):
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(3)
        self.bake_selaction_button = QPushButton("Bake selaction")
        self.button_layout.addWidget(self.bake_selaction_button, 0, 0, 1, 1)
        self.bake_selaction_button.clicked.connect(functools.partial(self.button_command, True, True))
        self.unbake_selaction_button = QPushButton("Unbake selaction")
        self.button_layout.addWidget(self.unbake_selaction_button, 1, 0, 1, 1)
        self.unbake_selaction_button.clicked.connect(functools.partial(self.button_command, True, False))
        self.bake_all_button = QPushButton("Bake all")
        self.button_layout.addWidget(self.bake_all_button, 0, 1, 1, 1)
        self.bake_all_button.clicked.connect(functools.partial(self.button_command, False, True))
        self.unbake_all_button = QPushButton("Unbake all")
        self.button_layout.addWidget(self.unbake_all_button, 1, 1, 1, 1)
        self.unbake_all_button.clicked.connect(functools.partial(self.button_command, False, False))
        self.verticalLayout.addLayout(self.button_layout)

    def button_command(self, to_selection, bake):
        ctrl = self.get_controller()
        if to_selection:
            dynamics_curves = self.get_curve_from_control(ctrl)
        else:
            dynamics_curves = self.get_all_dynamics_curves(ctrl)
        if bake:
            self.bake_curves(dynamics_curves)
        else:
            self.unbake_curves(dynamics_curves)

    def get_controller(self):
        try:
            return cmds.ls(sl=True)[0]
        except IndexError:
            cmds.error("Necessary to select character`s controller!")

    def bake_curves(self, curve_list):
        start_time, end_time = self.get_time_range()
        self.set_time_range(start_time, end_time)
        curve_blends = [[] for x in range(len(curve_list))]
        for frame in xrange(int(start_time), int(end_time + 2)):
            if frame > int(start_time + 1):
                for i, each_curve in enumerate(curve_list):
                    duplicate_curve = cmds.duplicate(curve_list[i], name=curve_list[i] + str(i))[0]
                    curve_blends[i].append(duplicate_curve)
            cmds.currentTime(frame, edit=True)
        for i, each_curve in enumerate(curve_list):
            blend_shape = cmds.blendShape(curve_blends[i], each_curve, inBetween=True, origin="world")[0]
            weight_attr = cmds.listAttr(blend_shape + ".w", m=True)[0]
            cmds.setKeyframe(blend_shape + "." + weight_attr, value=1, time=end_time, outTangentType="linear",
                             inTangentType="linear")
            cmds.setKeyframe(blend_shape + "." + weight_attr, value=0, time=start_time, outTangentType="linear",
                             inTangentType="linear")
        self.set_time_range(start_time, end_time)

    def unbake_curves(self, dynamics_curves):
        for each_curve in dynamics_curves:
            history = cmds.listHistory(each_curve, levels=1)
            try:
                blend_node = cmds.ls(history, type="blendShape")[0]
                connections = cmds.listConnections(blend_node)
                # delete blands curves and blandShape nod
                for each in connections:
                    if cmds.nodeType(each) == "transform" and each != each_curve:
                        cmds.delete(each)
                cmds.delete(blend_node)
            except IndexError:
                cmds.error("This object has no cache!")

    def get_all_dynamics_curves(self, ctrl):
        char_pfx = re.findall(r"(^[A-Za-z0-9_]*):", ctrl)[0]
        all_follicle = [x for x in cmds.ls(type='follicle') if char_pfx + ":" in x]
        dyn_curves = []
        for follicle in all_follicle:
            dyn_curve_shape = cmds.connectionInfo(follicle + ".outCurve", destinationFromSource=True)[0].split('.')[
                0]
            dyn_curve = cmds.listRelatives(dyn_curve_shape, parent=True)[0]
            dyn_curves.append(dyn_curve)
        return dyn_curves

    def get_curve_from_control(self, ctrl):
        if cmds.objExists(ctrl + ".prefix"):
            pfx_attr = cmds.getAttr(ctrl + ".prefix")
            name_space = ctrl.split(pfx_attr)[0]
            return [name_space + pfx_attr + "Dynamics_crv", ]
        else:
            cmds.error("Selected object is not part of the dynamic system !")

    def get_time_range(self):
        end_time = cmds.playbackOptions(q=True, max=True)
        start_time = cmds.playbackOptions(q=True, min=True)
        return start_time, end_time

    def set_time_range(self, start_time, end_time):
        ctrl = self.get_controller()
        nucleus = self.get_nuclius(ctrl)
        cmds.setAttr(nucleus + ".startFrame", start_time)
        cmds.playbackOptions(e=True, min=start_time)
        cmds.playbackOptions(e=True, max=end_time)
        cmds.currentTime(start_time, edit=True)

    def get_nuclius(self, ctrl):
        char_pfx = re.findall(r"(^[A-Za-z0-9_]*):", ctrl)[0]
        nucleus = [x for x in cmds.ls(type='nucleus') if char_pfx + ":" in x][0]
        return nucleus

    def text_dialog(self, text_type):
        help_dialog = QMessageBox()
        help_dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        if text_type == "Help":
            help_dialog.setWindowTitle("Help window")
            help_dialog.setText(HELP_TEXT)
        else:
            help_dialog.setWindowTitle("About program")
            help_dialog.setText(ABOUT_SCRIPT)
        help_dialog.setStandardButtons(QMessageBox.Cancel)
        help_dialog.exec_()

def bake_strand():
    global bake_win
    try:
        bake_win.deleteLater()
    except NameError:
        pass

    # app = QApplication([])
    bake_win = BakeStrand()
    bake_win.show()
    # app.exec_()


bake_strand()













