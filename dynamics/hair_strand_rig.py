from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import functools
import maya.cmds as cmds
import maya.mel as mm
import logging
from an_classControllers import AnControllers
from an_Procedures.joints import jntOnCurvNonSpline
from an_Procedures.connect import an_connectRigVis
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin # for parent ui to maya

ABOUT_SCRIPT = "\n" \
               "Latest updates:                               \n" \
               "3.02.2021     -add attribut prefix to control \n" \
               "27.01.2021    -start writing                  \n" \
               "                                              \n" \
               "Created by Andrey Belyaev                     \n" \
               "andreikin@mail.ru"

HELP_LABEL = "Select a chain of bones (more than two joints) on the basis of which will be\n" \
             "created FK controllers  and a dynamic curve\n"

HELP_TEXT = "\n" \
            "1 Build the bone chain by placing the joints where the controllers should be.\n" \
            "2 Adjust their orientation - the controllers will be oriented in a similar way\n" \
            "3 Make sure the bones are out of the collision objects \n" \
            "4 The root joint must have a parent, to which the system will be attached later\n" \
            "5 Choose 'Create dynanmics sistem'\n" \
            "\n" \
            "To create controllers on a switch - select the nucleus, then the switch and\n" \
            "press the button 'Connect nucleus'"

DEFAULT_PREFIX = "hairsStrand"
MAX_VERTEX_NUM = 40
DEFAULT_VERTEX_NUM = 4
MAX_JOINT_NUM = 40
DEFAULT_JOINT_NUM = 12
POINT_NUM_IN_DYN_CONSTRAINT = 2


class HairStrand_UI(MayaQWidgetBaseMixin, QMainWindow):
    def __init__(self):
        super(HairStrand_UI, self).__init__()
        self.setWindowTitle("Hair strand rigging system")
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.__menu_bar()  # help and About script windows
        self.__libel()  # text on top
        self.__option_box()
        self.__buttons()

    def __menu_bar(self):
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu = QMenu("Help")
        menu_bar.addMenu(menu)
        help_action = QAction("Help", self)
        menu.addAction(help_action)
        help_action.triggered.connect(functools.partial(self.text_dialog, "Help"))
        about_script_action = QAction("About script", self)
        menu.addAction(about_script_action)
        about_script_action.triggered.connect(functools.partial(self.text_dialog, "ABOUT_PROGRAM"))

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

    def __libel(self):
        self.help_label = QLabel(HELP_LABEL)
        self.verticalLayout.addWidget(self.help_label)

    def __option_box(self):
        self.option_box = QGroupBox("Options:")
        self.option_box_layout = QVBoxLayout(self.option_box)
        # text line Prefix
        self.pfx_layout = QHBoxLayout()
        self.pfx_label = QLabel("Prefix:")
        self.pfx_layout.addWidget(self.pfx_label)
        self.pfx_lineEdit = QLineEdit(DEFAULT_PREFIX)
        regexp = QRegExp('^([A-Za-z_]+[0-9]+)$')
        validator = QRegExpValidator(regexp)
        self.pfx_lineEdit.setValidator(validator)
        self.pfx_layout.addWidget(self.pfx_lineEdit)
        self.option_box_layout.addLayout(self.pfx_layout)       

        # slider Points number
        self.curve_hLayout = QHBoxLayout()
        self.curve_label = QLabel("Points number :")
        self.curve_hLayout.addWidget(self.curve_label)
        self.curve_horizontal_slider = QSlider()
        self.curve_horizontal_slider.setMinimum(1)
        self.curve_horizontal_slider.setMaximum(MAX_VERTEX_NUM)
        self.curve_horizontal_slider.setSliderPosition(DEFAULT_VERTEX_NUM)
        self.curve_horizontal_slider.setOrientation(Qt.Horizontal)
        self.curve_hLayout.addWidget(self.curve_horizontal_slider)
        self.curve_spin_box = QSpinBox()
        self.curve_spin_box.setMinimum(1)
        self.curve_spin_box.setMaximum(MAX_VERTEX_NUM)
        self.curve_spin_box.setValue(DEFAULT_VERTEX_NUM)
        self.curve_hLayout.addWidget(self.curve_spin_box)
        self.curve_horizontal_slider.valueChanged.connect(self.curve_spin_box.setValue)
        self.curve_spin_box.valueChanged.connect(self.curve_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.curve_hLayout)
        # slider Joints number
        self.horizontalLayout_2 = QHBoxLayout()
        self.joints_label = QLabel("Joints number :")
        self.horizontalLayout_2.addWidget(self.joints_label)
        self.joints_horizontal_slider = QSlider()
        self.joints_horizontal_slider.setMinimum(3)
        self.joints_horizontal_slider.setMaximum(MAX_JOINT_NUM)
        self.joints_horizontal_slider.setSliderPosition(DEFAULT_JOINT_NUM)
        self.joints_horizontal_slider.setOrientation(Qt.Horizontal)
        self.horizontalLayout_2.addWidget(self.joints_horizontal_slider)
        self.joints_spin_box = QSpinBox()
        self.joints_spin_box.setObjectName(u"joints_spin_box")
        self.joints_spin_box.setMinimum(3)
        self.joints_spin_box.setMaximum(MAX_JOINT_NUM)
        self.joints_spin_box.setValue(DEFAULT_JOINT_NUM)
        self.horizontalLayout_2.addWidget(self.joints_spin_box)
        self.joints_horizontal_slider.valueChanged.connect(self.joints_spin_box.setValue)
        self.joints_spin_box.valueChanged.connect(self.joints_horizontal_slider.setValue)
        self.option_box_layout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.option_box)

    def __buttons(self):
        self.buttons_layout = QHBoxLayout()
        self.connect_nucleus_button = QPushButton("Connect nucleus")
        self.buttons_layout.addWidget(self.connect_nucleus_button)
        self.connect_nucleus_button.clicked.connect(self.connect_nucleus)
        self.create_button = QPushButton("Create dynanmics system")
        self.buttons_layout.addWidget(self.create_button)
        self.verticalLayout.addLayout(self.buttons_layout)
        self.create_button.clicked.connect(self.create_rig)


class HairStrandRig(HairStrand_UI):
    def create_rig(self):
        self.get_data_from_ui()
        if self.get_objects_and_chek_it():
            self.rig_grp = cmds.group(empty=True, name=self.prefx + 'Rig_grp')
            self.fk_rigging()
            self.building_base_curve()
            self.building_dynamic_curve()
            self.fk_dynamics_mix_system()
            self.add_skin_joints()
            an_connectRigVis(self.rig_grp,
                             [self.input_curve, self.hair_sys, self.dyn_curve_grp, self.dyn_constraint, self.loc, ])

    def get_data_from_ui(self):
        self.prefx = self.pfx_lineEdit.text()
        if not self.prefx:
            logging.getLogger().warning("You did not enter a prefix, the default value will be used!")
            self.prefx = DEFAULT_PREFIX   
        self.point_number = self.curve_horizontal_slider.value()
        self.joint_number = self.joints_horizontal_slider.value()

    def get_objects_and_chek_it(self):
        self.joints = cmds.ls(sl=True)
        
        if cmds.objExists(self.prefx+'Rig_grp'):
            cmds.error("Scene already contains objects with this prefix, choose another ")
            
        if len(self.joints) < 3 :
            logging.getLogger().error("Necessary to select at least three joints!")
            return False
        for jnt in self.joints: 
            if not cmds.nodeType(jnt)=="joint": 
                cmds.error("Necessary to select at least three joints!")
                return False
        # get an object to which the entire system will be bound by the constraint
        try:
            self.parent_object = cmds.listRelatives(self.joints[0], parent=True)[0]
        except TypeError:
            self.parent_object = None
            logging.getLogger().warning("No parent, so the system will not be attached!")
        return True

    def fk_rigging(self):
        self.controls = []
        self.fk_grp = cmds.group(empty=True, name=self.prefx + 'FK_grp')
        cmds.parent(self.fk_grp, self.rig_grp)
        if self.parent_object:
            cmds.parentConstraint(self.parent_object, self.fk_grp)
        for i, jnt in enumerate(self.joints[:-1]):
            ctrl = AnControllers(self.prefx + str(i) + "_CT")
            ctrl.makeController(shapeType="fk", orient="X", pos=jnt)
            ctrl.hideAttr(['sx', 'sy', 'sz', 'v'])
            self.controls.append(ctrl)
            if i == 0:
                cmds.parent(ctrl.oriGrp, self.fk_grp)
            else:
                cmds.parent(ctrl.oriGrp, self.controls[i - 1].name)
            cmds.parentConstraint(ctrl.name, jnt)
            # add attribute to determine whether the controller belongs to dynamic system
            cmds.addAttr(ctrl.name, longName='prefix', dt='string', keyable=False)
            cmds.setAttr(ctrl.name + ".prefix", self.prefx, type="string")

    def building_base_curve(self):
        point_position = []
        for jnt in self.joints:
            jnt_coordinates = cmds.xform(jnt, query=True, translation=True, worldSpace=True)
            point_position.append(jnt_coordinates)
        self.base_curve = cmds.curve(p=point_position, degree=2, name=self.prefx + 'FK_crv')
        cmds.skinCluster(self.joints, self.base_curve, toSelectedBones=True, normalizeWeights=True)
        cmds.rebuildCurve(self.base_curve,
                          rebuildType=0,
                          spans=self.point_number,
                          constructionHistory=True)
        cmds.parent(self.base_curve, self.rig_grp)

    def building_dynamic_curve(self):
        self.input_curve = cmds.duplicate(name=self.prefx + 'Input_crv', inputConnections=True)[0]
        mm.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')
        crv_shape = cmds.listRelatives(self.input_curve, shapes=True)[1]
        # getting names of all dynamics objects and rename it
        follicle = cmds.listConnections(crv_shape + ".local")[0]
        follicle = cmds.rename(follicle, self.prefx + '_follicle')
        cmds.setAttr(follicle + ".pointLock", 0)
        fol_shape = cmds.listRelatives(follicle, shapes=True)[0]
        dyn_curve_shape = cmds.connectionInfo(fol_shape + ".outCurve", destinationFromSource=True)[0].split('.')[0]
        self.dyn_curve = cmds.listRelatives(dyn_curve_shape, parent=True)[0]
        self.hair_sys_shape = cmds.connectionInfo(fol_shape + ".outHair", destinationFromSource=True)[0].split('.')[0]
        self.hair_sys = cmds.listRelatives(self.hair_sys_shape, parent=True)[0]
        self.setup_mix_attribut()
        self.hair_sys = cmds.rename(self.hair_sys, self.prefx + '_hairSystem')
        self.dyn_curve_grp = cmds.listRelatives(self.dyn_curve, parent=True)[0]
        self.dyn_curve = cmds.rename(self.dyn_curve, self.prefx + 'Dynamics_crv')
        cmds.select(self.dyn_curve + '.cv[0:{}]'.format(POINT_NUM_IN_DYN_CONSTRAINT))
        dynamicConstraintShape = mm.eval('createNConstraint transform 0;')[0]
        self.dyn_constraint = cmds.listRelatives(dynamicConstraintShape, parent=True)[0]
        cmds.parentConstraint(self.controls[0].name, self.dyn_constraint)
        cmds.parent(self.hair_sys, self.dyn_curve_grp, self.dyn_constraint, self.rig_grp)

    def setup_mix_attribut(self):
        soft_suffix = "_soft"
        hard_suffix = "_hard"
        atributes = {"stretchResistance": (0, 200),
                     "compressionResistance": (0, 200),
                     "bendResistance": (0, 200),
                     "mass": (0, 10),
                     "drag": (0, 1),
                     "damp": (0, 10)}
        self.controls[0].addDevideAttr()
        driver_attr = self.controls[0].name
        cmds.addAttr(driver_attr, longName="stiffness", keyable=True, minValue=0, maxValue=1)
        for atrribut in atributes:
            default_val = cmds.getAttr(self.hair_sys_shape + "." + atrribut)
            cmds.addAttr(self.hair_sys,
                         longName=atrribut + soft_suffix,
                         keyable=True,
                         minValue=atributes[atrribut][0],
                         maxValue=atributes[atrribut][1],
                         defaultValue=default_val)
            cmds.addAttr(self.hair_sys,
                         longName=atrribut + hard_suffix,
                         keyable=True,
                         minValue=atributes[atrribut][0],
                         maxValue=atributes[atrribut][1],
                         defaultValue=default_val * 4)
            blend_node = cmds.createNode('blendTwoAttr', n=atrribut + 'Blend_nod')
            cmds.connectAttr(self.hair_sys + "." + atrribut + soft_suffix, blend_node + ".input[0]")
            cmds.connectAttr(self.hair_sys + "." + atrribut + hard_suffix, blend_node + ".input[1]")
            cmds.connectAttr(blend_node + ".output", self.hair_sys_shape + "." + atrribut)
            cmds.connectAttr(driver_attr + ".stiffness", blend_node + ".attributesBlender")

    def fk_dynamics_mix_system(self):
        cmds.addAttr(self.controls[0].name,
                     longName="fk_dyn_mix",
                     keyable=True,
                     minValue=0,
                     maxValue=1)
        bldShape = cmds.blendShape(self.dyn_curve, self.base_curve,
                                   origin="world",
                                   name=self.prefx + 'blendShape')[0]
        cmds.connectAttr(self.controls[0].name + ".fk_dyn_mix", bldShape + "." + self.dyn_curve)

    def add_skin_joints(self):
        self.loc, self.jointsNames, skin_jnt_grp = jntOnCurvNonSpline(self.base_curve, self.joint_number, self.prefx)
        cmds.parent(skin_jnt_grp, self.rig_grp)
        cmds.parent(self.loc, self.controls[0].name)
        an_connectRigVis(self.rig_grp, self.jointsNames)

    def connect_nucleus(self):
        try:
            nucleus, switch = cmds.ls(sl=True)
        except ValueError:
            logging.getLogger().error("Select nucleus, then switch  and click the 'connect' button ")
        cmds.addAttr(switch, ln="haer_dynamics", at="enum", en="off:on", keyable=True)
        cmds.connectAttr(switch + ".haer_dynamics", nucleus + ".enable")


def hair_strand_rig():
    global dyn_win
    try:
        dyn_win.deleteLater()
    except NameError:
        pass
    dyn_win = HairStrandRig()
    dyn_win.show()

if __name__ == '__main__':
    hair_strand_rig()












