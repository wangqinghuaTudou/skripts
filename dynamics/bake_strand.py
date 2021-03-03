from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import re
import functools
import logging
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin  # for parent ui to maya

ABOUT_SCRIPT = "\n" \
               "Latest updates:                          \n" \
               "                                         \n" \
               "03.03.2021   -add stop comand            \n" \
               "03.03.2021   -add start time offset      \n" \
               "12.02.2021   -refactoring                \n" \
               "03.02.2021   -start writing              \n" \
               "                                         \n" \
               "Created by Andrey Belyaev                \n" \
               "andreikin@mail.ru"

HELP_LABEL = "Select the required character dynamics controller and click bake dynamics. \n" \
             "After baking, you can fix problem points manually. "

HELP_TEXT = "\n" \
            "- Choose the character you want to work with by choosing one of his controllers.\n" \
            "- If you need to cache one dynamic system, click 'Bake_selaction'\n" \
            "- To cache all dynamic systems, choose 'Select all systems' than 'Bake_selaction'\n" \
            "- You can change the 'Stiffness' parameter on the root dynamic controller\n" \
            "- To avoid wasting resources and the appearance of warnings in the command line,\n" \
            "        turn off the dynamics on the main controller of the character"

START_TIME_OFFSET = 30

logging.basicConfig(format="%(asctime)s  line: %(lineno)s   - function  %(funcName)s() %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.WARNING)


class BakeStrand(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self):
        super(BakeStrand, self).__init__()
        self.baking_process=False
        # Window
        self.setWindowTitle("Bake strand system")
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.central_widget)

        # help and About script windows menu_bar
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

        # text on top
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)

        # buttons
        self.button_layout = QGridLayout()
        self.button_layout.setSpacing(3)
        self.bake_all_button = QPushButton("Select all systems")
        self.button_layout.addWidget(self.bake_all_button, 0, 0, 1, 1)
        self.bake_all_button.clicked.connect(self.select_all_dyn_controls)
        self.unbake_selaction_button = QPushButton("Unbake selaction")
        self.button_layout.addWidget(self.unbake_selaction_button, 0, 1, 1, 1)
        self.unbake_selaction_button.clicked.connect(functools.partial(self.button_command, False))
        self.bake_selaction_button = QPushButton("Bake selaction")
        self.button_layout.addWidget(self.bake_selaction_button, 0, 2, 1, 1)
        self.bake_selaction_button.clicked.connect(functools.partial(self.button_command, True))
        self.verticalLayout.addLayout(self.button_layout)
        logger.debug(" executed user interface")

    def button_command(self, bake):
        """
        Caches or removes dynamic cache.
        """
        controllers = self.get_controllers()
        dynamics_curves = []
        for ctrl in controllers:
            dyn_curve = self.get_dynamics_object_from_control(ctrl)[0]
            dynamics_curves.append(dyn_curve)
        if bake:
            self.bake_curves(dynamics_curves)
        else:
            self.unbake_curves(dynamics_curves)
        logger.debug("Action completed successfully")

    def get_controllers(self):
        selections = cmds.ls(sl=True)
        if selections:
            return selections
        else:
            cmds.error("Necessary to select character`s controller!")

    def stop_baking(self):
        self.baking_process=False
    
    
    def button_changer(self, is_baking):
        """
        Changes the functionality of the button during baking.
        """
        self.bake_selaction_button.clicked.disconnect()
        if is_baking:
            self.bake_selaction_button.clicked.connect(self.stop_baking)
            self.bake_selaction_button.setStyleSheet('QPushButton {background-color: red;}')
            self.bake_selaction_button.setText("Stop baking")
        else:
            self.bake_selaction_button.clicked.connect(functools.partial(self.button_command, True))
            self.bake_selaction_button.setStyleSheet('QPushButton {background-color: light gray;}')
            self.bake_selaction_button.setText("Bake selaction")
    
    def bake_curves(self, curve_list):
        logger.debug(" started")
        self.baking_process=True
        start_time, end_time = self.get_time_range()
        start_time -= START_TIME_OFFSET
        self.set_time_range(start_time, end_time)
        curve_blends = [[] for x in range(len(curve_list))]
        for frame in xrange(int(start_time), int(end_time + 2)):
            if self.baking_process:
                if frame > int(start_time + 1):
                    for i, each_curve in enumerate(curve_list):
                        qApp.processEvents() #checks the state of the interface while it is baiking 
                        self.button_changer (is_baking = True)
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
        self.set_time_range(start_time+START_TIME_OFFSET, end_time)
        self.button_changer (is_baking = False)

    def unbake_curves(self, dynamics_curves):
        logger.debug(" started")
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
                cmds.warning("Curve {} has no cache!".format(each_curve))

    def get_dynamics_object_from_control(self, ctrl):
        logger.debug(" started")
        name_space, pfx_attr = self.get_character_namespace_and_prefix(ctrl)
        prefix = name_space + pfx_attr
        # get dyn_curve, hair_system, nucleus
        if cmds.objExists(prefix + "Dynamics_crv") and cmds.objExists(prefix + "_hairSystem"):
            dyn_curve = prefix + "Dynamics_crv"
            hair_system = prefix + "_hairSystem"
            nucleus = \
            [x for x in cmds.listHistory(hair_system + 'Shape', future=True) if cmds.nodeType(x) == "nucleus"][0]
        else:
            cmds.error("No dynamic system associated with the controller ")
        return dyn_curve, hair_system, nucleus

    def get_character_namespace_and_prefix(self, ctrl):
        if cmds.objExists(ctrl + ".prefix"):
            pfx_attr = cmds.getAttr(ctrl + ".prefix")
            name_space = ctrl.split(pfx_attr)[0]
            return name_space, pfx_attr
        else:
            cmds.error("Selected object is not part of the dynamic system !")

    def get_time_range(self):
        end_time = cmds.playbackOptions(q=True, max=True)
        start_time = cmds.playbackOptions(q=True, min=True)
        return start_time, end_time

    def set_time_range(self, start_time, end_time):
        logger.debug(" started")
        ctrl = self.get_controllers()[0]
        dyn_curve, hair_system, nucleus = self.get_dynamics_object_from_control(ctrl)
        cmds.setAttr(nucleus + ".startFrame", start_time)
        cmds.playbackOptions(e=True, min=start_time)
        cmds.playbackOptions(e=True, max=end_time)
        cmds.currentTime(start_time, edit=True)

    def text_dialog(self, text_type):
        logger.debug(" started")
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

    def select_all_dyn_controls(self):
        logger.debug(" started")
        ctrl = self.get_controllers()[0]
        name_space, pfx_attr = self.get_character_namespace_and_prefix(ctrl)
        formula = re.compile(name_space + "\w+_CT$")
        all_controllers = [x for x in cmds.ls() if formula.match(x)]
        controllers = [x for x in all_controllers if cmds.objExists(x + ".fk_dyn_mix")]
        cmds.select(controllers)


def bake_strand():
    global bake_win
    try:
        bake_win.deleteLater()
    except NameError:
        pass
    bake_win = BakeStrand()
    bake_win.show()


if __name__ == '__main__':
    bake_strand()
